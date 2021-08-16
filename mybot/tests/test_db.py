import pytest
from azure.storage.table import TableService
import lebowski.azure_connections as connector


@pytest.fixture()
def empty_tables():
    akv = connector.AKVConnector(tenant_id="Not used", client_id="Not used", client_secret="Not used", env="dev")
    storage_account = TableService(connection_string=akv.get_storage_connection_string(), is_emulated=True)
    for table_name in ["spendings", "mileage", "reminders"]:
        storage_account.create_table(table_name)

    tables = storage_account.list_tables()

    yield storage_account

    # tear down
    for t in tables:
        storage_account.delete_table(t.name)

def test_add_gas_spending(empty_tables: TableService):
    customer = {'PartitionKey': 'Harp', 'RowKey': '1', 'email' : 'harp@contoso.com', 'phone' : '555-555-5555'}
    empty_tables.insert_entity("spendings", customer)
    entity = empty_tables.get_entity("spendings", partition_key='Harp', row_key='1')
    assert entity['email'] == 'harp@contoso.com'