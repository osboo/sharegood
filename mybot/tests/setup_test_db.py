import argparse
from azure.storage.table import TableService
from lebowski.azure_connections import AKVConnector
from tests.test_db import setup_test_db, tear_down_test_db


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    args = parser.parse_args()
    if args.command == 'init':
        setup_test_db()
    elif args.command == 'clean':
        akv = AKVConnector("Not used", "Not used", "Not used", env="dev")
        connection_string = akv.get_storage_connection_string()
        storage_account = TableService(connection_string=connection_string)
        tear_down_test_db(storage_account)
    else:
        raise Exception("Unknown command: '%s'" % args)
