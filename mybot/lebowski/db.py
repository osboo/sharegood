import time
from lebowski.enums import Tables, Categories
from azure.storage.table import TableService


class DBHelper():
    def __init__(self, table_connector: TableService) -> None:
        self.table_connector = table_connector


    def get_new_key(self, user_id:int) -> str:
        t = time.time()
        return str(user_id) + ":" + "{:.3f}".format(20000000000 - t)


    def add_gas_record(self, user_id: int, amount: float, ccy: str, volume: float = None) -> str:
        key = self.get_new_key(user_id)
        entity = {
            "PartitionKey": Categories.GAS, "RowKey": key, "amount" : amount, "ccy" : ccy
        }
        volume_str = None
        if volume is not None:
            entity["volume"] = volume
            volume_str = "{:.2f}".format(volume)
        self.table_connector.insert_entity(Tables.SPENDINGS, entity)        
        return f"key: {key}, amount: {amount}, ccy: {ccy}, volume: {volume_str} л."
    

    def add_mileage_record(self, user_id: int, mileage: float) -> str:
        key = self.get_new_key(user_id)
        entity = {
            "PartitionKey": Categories.MILEAGE, "RowKey": key, "mileage" : mileage
        }
        self.table_connector.insert_entity(Tables.MILEAGE, entity)
        return f"key: {key}, mileage: {mileage}"


    def add_car_goods_record(self, user_id: int, amount: float, ccy: str, description: str) -> str:
        key = self.get_new_key(user_id)
        entity = {
            "PartitionKey": Categories.CAR_GOODS, "RowKey": key, "amount": amount, "ccy": ccy, "description": description
        }
        self.table_connector.insert_entity(Tables.SPENDINGS, entity)
        return f"key: {key}, amount: {amount}, ccy: {ccy}, description: {description}"


    def add_car_repair_record(self, user_id: int, amount: float, ccy: str, description: str) -> str:
        key = self.get_new_key(user_id)
        entity = {
            "PartitionKey": Categories.REPAIR, "RowKey": key, "amount": amount, "ccy": ccy, "description": description
        }
        self.table_connector.insert_entity(Tables.SPENDINGS, entity)
        return f"key: {key}, amount: {amount}, ccy: {ccy}, description: {description}"


    def add_mileage_reminder_record(self, user_id: int, mileage: int, description: str) -> str:
        index = self.get_mileage_reminders_count(user_id) + 1
        key = self.get_new_key(user_id)
        entity = {
            "PartitionKey": Categories.REMINDER_MILEAGE, "RowKey": key, "TargetMileage": mileage, "description": description, "index": index
        }
        self.table_connector.insert_entity(Tables.REMINDERS, entity)
        return f"key: {key}, target mileage: {mileage}, description: {description}"


    def get_mileage_reminders_count(self, user_id: int) -> int:
        try:
            test_moment_key = self.get_new_key(user_id)
            last_reminder_index_list = list(self.table_connector.query_entities(table_name=Tables.REMINDERS,
                filter=f"PartitionKey eq '{Categories.REMINDER_MILEAGE}' and RowKey gt '{test_moment_key}'",
                num_results=1))
            result = last_reminder_index_list[0]['index']
        except:
            result = 0
        return result

