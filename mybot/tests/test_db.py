import logging
import pytest
from azure.storage.table import TableService
from lebowski.azure_connections import AKVConnector
from lebowski.db import DBHelper
from lebowski.enums import CCY, Tables, Categories


def setup_test_db():
    akv = AKVConnector("Not used", "Not used", "Not used", env="dev")
    connection_string = akv.get_storage_connection_string()
    logger = logging.getLogger("unit-tests")
    logger.setLevel(logging.INFO)
    logger.info("Connection String " + connection_string)
    storage_account = TableService(connection_string=connection_string)
    for table_name in [Tables.SPENDINGS, Tables.MILEAGE, Tables.REMINDERS]:
        storage_account.create_table(table_name)
    return storage_account 



def tear_down_test_db(storage_account: TableService):
    for t in [Tables.SPENDINGS, Tables.MILEAGE, Tables.REMINDERS]:
        storage_account.delete_table(t)


@pytest.fixture()
def empty_tables():
    storage_account = setup_test_db()

    yield storage_account

    # tear down
    tear_down_test_db(storage_account)

def test_add_gas_spending(empty_tables: TableService):
    db = DBHelper(empty_tables)
    db.add_gas_record("123", 30, CCY.BYN)
    test_moment_key = db.get_new_key("123")
    entities = empty_tables.query_entities(Tables.SPENDINGS, filter=f"PartitionKey eq '{Categories.GAS}' and RowKey gt '{test_moment_key}' and RowKey lt '123:20000000000'")
    result = [e for e in entities]
    assert len(result) == 1
    assert result[0]['amount'] == 30.0


def test_add_mileage(empty_tables: TableService):
    db = DBHelper(empty_tables)
    db.add_mileage_record("123", 124302)
    test_moment_key = db.get_new_key("123")
    entities = empty_tables.query_entities(Tables.MILEAGE, filter=f"PartitionKey eq '{Categories.MILEAGE}' and RowKey gt '{test_moment_key}' and RowKey lt '123:20000000000'")
    result = [e for e in entities]
    assert len(result) == 1
    assert result[0]['mileage'] == 124302.0


def test_add_car_goods_float(empty_tables: TableService):
    db = DBHelper(empty_tables)
    db.add_car_goods_record(123, 10.05, CCY.BYN, "огнетушитель")
    test_moment_key = db.get_new_key("123")
    entities = empty_tables.query_entities(Tables.SPENDINGS, filter=f"PartitionKey eq '{Categories.CAR_GOODS}' and RowKey gt '{test_moment_key}' and RowKey lt '123:20000000000'")
    result = [e for e in entities]
    assert len(result) == 1
    assert result[0]['amount'] == 10.05
    assert result[0]['ccy'] == CCY.BYN


def test_add_car_goods_int(empty_tables: TableService):
    db = DBHelper(empty_tables)
    db.add_car_goods_record(123, 10.0, CCY.BYN, "огнетушитель")
    test_moment_key = db.get_new_key("123")
    entities = empty_tables.query_entities(Tables.SPENDINGS, filter=f"PartitionKey eq '{Categories.CAR_GOODS}' and RowKey gt '{test_moment_key}' and RowKey lt '123:20000000000'")
    result = [e for e in entities]
    assert len(result) == 1
    try:
        amount = result[0]['amount'] / 1.0
    except Exception:
        amount = result[0]['amount'].value
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
