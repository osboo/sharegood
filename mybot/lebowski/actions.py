from lebowski.db import DBHelper
from azure.storage.table import TableService

def add_gas_action(args: list, storage: TableService, user_id: int):
    [amount, ccy, volume] = args
    db = DBHelper(storage)
    db.add_gas_record(user_id, amount, ccy, volume)