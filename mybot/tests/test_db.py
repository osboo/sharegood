import pytest
import logging
from azure.storage.table import TableService
from lebowski.azure_connections import AKVConnector
from lebowski.db import DBHelper
from lebowski.enums import CCY, Tables


@pytest.fixture()
def empty_tables():
    akv = AKVConnector("Not used", "Not used", "Not used", env="dev")
    storage_account = TableService(connection_string=akv.get_storage_connection_string())
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info("Connection String " + akv.get_storage_connection_string())
    for table_name in [Tables.SPENDINGS, Tables.MILEAGE, Tables.REMINDERS]:
        storage_account.create_table(table_name)

    tables = storage_account.list_tables()

    yield storage_account

    # tear down
    for t in tables:
        storage_account.delete_table(t.name)

def test_add_gas_spending(empty_tables: TableService):
    db = DBHelper(empty_tables)
    db.add_gas_record("123", 30, CCY.BYN)
    test_moment_key = db.get_new_key("123")
    entities = empty_tables.query_entities(Tables.SPENDINGS, filter=f"PartitionKey eq 'gas' and RowKey gt '{test_moment_key}' and RowKey lt '123:20000000000'")
    result = [e for e in entities]
    assert len(result) == 1
    assert result[0]['amount'] == 31.0