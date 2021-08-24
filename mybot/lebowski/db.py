import time
from lebowski.enums import Tables
from azure.storage.table import TableService


class DBHelper():
    def __init__(self, table_connector: TableService) -> None:
        self.table_connector = table_connector

    def get_new_key(self, user_id:int) -> str:
        t = time.time()
        return str(user_id) + ":" + str((20000000000 - t))

    def add_gas_record(self, user_id: int, amount: float, ccy: str, volume: float = None) -> None:
        key = self.get_new_key(user_id)
        entity = {
            "PartitionKey": "gas", "RowKey": key, "amount" : amount, "ccy" : ccy
        }
        if volume is not None:
            entity["volume"] = volume
        self.table_connector.insert_entity(Tables.SPENDINGS, entity)
        return key