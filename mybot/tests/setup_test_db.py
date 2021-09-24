import argparse
from azure.storage.table import TableService
from lebowski.azure_connections import AKVConnector
from tests.test_db import setup_test_db, tear_down_test_db


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('--payload', help='path to directory with datatable. Every csv file will be saved into table with corresponding name of csv file')
    args = parser.parse_args()
    if args.command == 'init':        
        setup_test_db(args.payload)
    elif args.command == 'clean':
        tear_down_test_db()
    else:
        raise Exception("Unknown command: '%s'" % args)
