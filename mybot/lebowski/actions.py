import logging
from azure.storage.table import TableService
from lebowski.db import DBHelper
from lebowski.azure_connections import AKVConnector
from lebowski.external_api import get_eur_rate, get_gas_quotes
from lebowski.enums import CCY


def add_gas_action(args: list, storage: TableService, user_id: int, akv: AKVConnector):
    [amount, ccy, volume] = args
    db = DBHelper(storage)
    if volume is None:
        try:
            price_eur = get_gas_quotes(akv.get_gas_quotes_api_token())
            if ccy != CCY.EUR:
                rate = get_eur_rate(akv.get_fx_quotes_api_token(), ccy)
            else:
                rate = 1.0

            volume = amount / rate / price_eur
        except Exception as e:
            logging.error(e)
            volume = None
    db.add_gas_record(user_id, amount, ccy, volume)