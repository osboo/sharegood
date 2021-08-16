import time
from azure.storage.table import TableService


class DBHelper():
    def __init__(self, table_connector: TableService) -> None:
        self.table_connector = table_connector

    def get_now_key() -> str:
        t = time.time()
        return str((20000000000 - t))

    def add_gas_record(self, user_id: str, amount: float, ccy: str, volume: float = None) -> None:
        entity = {
            'PartitionKey': 'gas', 'RowKey': f'{user_id + ":" + self.get_now_key()}', 'amount' : amount, 'ccy' : ccy
        }
        if volume is not None:
            entity
        pass