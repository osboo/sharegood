import logging
import os

import pandas as pd
import pytest
from azure.storage.table import TableService
from lebowski.azure_connections import AKVConnector
from lebowski.db import DBHelper
from lebowski.enums import CCY, Categories, Tables
from lebowski.stat import (convert_spendings_to_eur, get_total_mileage,
                           get_total_spending_eur)


def load_from_csv(relative_path: str, storage_account: TableService):
    filenames = os.listdir(relative_path)
    for filename in filenames:
        if filename.endswith(".csv"):
            table_name = filename[:-4]
            storage_account.create_table(table_name)
            df = pd.read_csv(os.path.join(relative_path, filename))
            for _, row in df.iterrows():
                d = pd.Series.to_dict(row)
                entity = {}
                for k, v in d.items():
                    if k == 'Timestamp' or k.endswith('@type'):
                        pass
                    else:
                        entity[k] = v
                storage_account.insert_entity(table_name, entity)


def setup_test_db(path: str):
    storage_account = get_test_storage()
    if path is None:
        table_names = [Tables.SPENDINGS, Tables.MILEAGE, Tables.REMINDERS]
        for table_name in table_names:
            storage_account.create_table(table_name)
    else:
        load_from_csv(path, storage_account)
    return storage_account


def get_test_storage() -> TableService:
    akv = AKVConnector("Not used", "Not used", "Not used", env="dev")
    connection_string = akv.get_storage_connection_string()
    logger = logging.getLogger("unit-tests")
    logger.setLevel(logging.INFO)
    logger.info("Connection String " + connection_string)
    storage_account = TableService(connection_string=connection_string)
    return storage_account


def tear_down_test_db():
    storage_account = get_test_storage()
    for t in storage_account.list_tables():
        storage_account.delete_table(t.name)


@pytest.fixture()
def empty_tables():
    tear_down_test_db()
    storage_account = setup_test_db(None)

    yield storage_account

    # tear down
    tear_down_test_db()


@pytest.fixture()
def dump1_tables():
    tear_down_test_db()
    storage_account = setup_test_db("mybot/tests/test-data/dump1")

    yield storage_account

    # tear down
    tear_down_test_db()


@pytest.fixture()
def dump1_dataframes_and_rates():
    tear_down_test_db()
    storage_account = setup_test_db("mybot/tests/test-data/dump1")
    db = DBHelper(storage_account)
    d = db.get_stat_data(user_id=229598673)

    rates = {
        CCY.BYN: 2.93,
        CCY.RUB: 85.30,
        CCY.USD: 1.17
    }
    yield (d, rates)

    # tear down
    tear_down_test_db()


def test_add_gas_spending(empty_tables: TableService):
    db = DBHelper(empty_tables)
    db.add_gas_record("123", 30, CCY.BYN)
    test_moment_key = db.get_new_key("123")
    entities = empty_tables.query_entities(
        Tables.SPENDINGS, filter=f"PartitionKey eq '{Categories.GAS}' and RowKey gt '{test_moment_key}' and RowKey lt '123:20000000000'")
    result = [e for e in entities]
    assert len(result) == 1
    assert db.get_float_value(result[0]['amount']) == 30.0


def test_add_mileage(empty_tables: TableService):
    db = DBHelper(empty_tables)
    db.add_mileage_record("123", 124302)
    test_moment_key = db.get_new_key("123")
    entities = empty_tables.query_entities(
        Tables.MILEAGE, filter=f"PartitionKey eq '{Categories.MILEAGE}' and RowKey gt '{test_moment_key}' and RowKey lt '123:20000000000'")
    result = [e for e in entities]
    assert len(result) == 1
    assert result[0]['mileage'] == 124302.0


def test_add_car_goods_float(empty_tables: TableService):
    db = DBHelper(empty_tables)
    db.add_car_goods_record(123, 10.05, CCY.BYN, "огнетушитель")
    test_moment_key = db.get_new_key("123")
    entities = empty_tables.query_entities(
        Tables.SPENDINGS, filter=f"PartitionKey eq '{Categories.CAR_GOODS}' and RowKey gt '{test_moment_key}' and RowKey lt '123:20000000000'")
    result = [e for e in entities]
    assert len(result) == 1
    assert result[0]['amount'] == 10.05
    assert result[0]['ccy'] == CCY.BYN


def test_add_car_goods_int(empty_tables: TableService):
    db = DBHelper(empty_tables)
    db.add_car_goods_record(123, 10.0, CCY.BYN, "огнетушитель")
    test_moment_key = db.get_new_key("123")
    entities = empty_tables.query_entities(
        Tables.SPENDINGS, filter=f"PartitionKey eq '{Categories.CAR_GOODS}' and RowKey gt '{test_moment_key}' and RowKey lt '123:20000000000'")
    result = [e for e in entities]
    assert len(result) == 1
    amount = db.get_float_value(result[0]['amount'])
    assert amount == 10.0
    assert result[0]['ccy'] == CCY.BYN


def test_get_reminders_count(empty_tables: TableService):
    db = DBHelper(empty_tables)
    actual = db.get_mileage_reminders_count(123)
    assert actual == 0
    db.add_mileage_reminder_record(123, 123, "reminder 1")
    actual = db.get_mileage_reminders_count(123)
    assert actual == 1
    db.add_mileage_reminder_record(123, 456, "reminder 2")
    actual = db.get_mileage_reminders_count(123)
    assert actual == 2


def test_current_mileage(empty_tables: TableService):
    db = DBHelper(empty_tables)
    assert db.get_current_mileage(123) == 0
    db.add_mileage_record(123, 421000)
    db.add_mileage_record(123, 421001)
    db.add_mileage_record(123, 421002)
    assert db.get_current_mileage(123) == 421002


def test_expired_notification(empty_tables: TableService):
    db = DBHelper(empty_tables)
    db.add_mileage_record(123, 10)
    db.add_mileage_reminder_record(123, 45, "Поменять цвет волос на 45")
    db.add_mileage_reminder_record(123, 110, "Whatever")
    db.add_mileage_record(123, 100)
    reminders = db.list_reminders(123)
    assert "Уже наступило" in reminders[1]


@pytest.mark.parametrize(
    "user_id,expected_length",
    [
        (229598672, 2),
        (229598673, 4),
        (229598674, 2)
    ]
)
def test_extract_history_by_user_id(dump1_tables: TableService, user_id: int, expected_length: int):
    db = DBHelper(dump1_tables)
    df = db.extract_history_by_user_id(Tables.MILEAGE, user_id=user_id)
    assert len(df) == expected_length


def test_stat_spendings(dump1_dataframes_and_rates: tuple):
    d = dump1_dataframes_and_rates[0]
    rates = dump1_dataframes_and_rates[1]
    df_spendings_eur = convert_spendings_to_eur(d[Tables.SPENDINGS], rates)
    total_spending = get_total_spending_eur(df_spendings_eur)        
    assert abs(total_spending - 698.14) <= 1e-2


def test_stat_mileage(dump1_dataframes_and_rates: tuple):    
    d = dump1_dataframes_and_rates[0]
    total_mileage = get_total_mileage(d[Tables.MILEAGE])
    assert total_mileage == 124190 - 123033