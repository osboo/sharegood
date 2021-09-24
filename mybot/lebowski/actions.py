import logging

from azure.storage.table import TableService

from lebowski.azure_connections import AKVConnector
from lebowski.db import DBHelper
from lebowski.enums import CCY, Tables
from lebowski.external_api import get_eur_rates, get_gas_quotes
from lebowski.stat import convert_spendings_to_eur, get_total_mileage, get_total_spending_eur


def add_gas_action(args: list, storage: TableService, user_id: int, akv: AKVConnector) -> str:
    [amount, ccy, volume] = args
    db = DBHelper(storage)
    if volume is None:
        try:
            price_eur = get_gas_quotes(akv.get_gas_quotes_api_token())
            if ccy != CCY.EUR:
                rate = get_eur_rates(akv.get_fx_quotes_api_token())[ccy]
            else:
                rate = 1.0

            volume = amount / rate / price_eur
        except Exception as e:
            logging.error(e)
            volume = None
    return db.add_gas_record(user_id, amount, ccy, volume)


def add_mileage_action(args: list, storage: TableService, user_id: int, akv: AKVConnector) -> str:
    [mileage] = args
    db = DBHelper(storage)
    adding_mileage_report = db.add_mileage_record(user_id, mileage)

    result_list = []
    result_list.append(adding_mileage_report)
    reminders = db.list_reminders(user_id)
    for r in reminders:
        if "Уже наступило" in r:
            result_list.append(r)

    return "\n".join(result_list)

def add_car_goods_action(args: list, storage: TableService, user_id, akv: AKVConnector) -> str:
    [amount, ccy, description] = args
    db = DBHelper(storage)
    return db.add_car_goods_record(user_id, amount, ccy, description)


def add_car_repair_action(args: list, storage: TableService, user_id, akv: AKVConnector) -> str:
    [amount, ccy, description] = args
    db = DBHelper(storage)
    return db.add_car_repair_record(user_id, amount, ccy, description)


def add_mileage_reminder_action(args: list, storage: TableService, user_id: int, akv: AKVConnector) -> str:
    [target_mileage, description] = args
    db = DBHelper(storage)
    return db.add_mileage_reminder_record(user_id, target_mileage, description)


def compute_stat_action(dataset: dict, akv: AKVConnector) -> dict:
    result = {}

    result['total_mileage'] = get_total_mileage(dataset[Tables.MILEAGE])

    try:
        rates = get_eur_rates(akv.get_fx_quotes_api_token())
    except Exception as e:
        logging.error(e)
        rates = {
            CCY.BYN: 2.93,
            CCY.RUB: 85.30,
            CCY.USD: 1.17
        }
    df_spendings_eur = convert_spendings_to_eur(dataset[Tables.SPENDINGS], rates)
    result['total_spending'] = get_total_spending_eur(df_spendings_eur)
    result['km_cost'] = result['total_spending'] / result['total_mileage'] if result['total_mileage'] > 0 else 0.0
    return result
