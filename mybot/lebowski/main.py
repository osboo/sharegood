import logging
import os

import azure.functions as func
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ParseMode
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import bold, text
from azure.storage.table import TableService
from babel import numbers
from middlewares.access import AccessMiddleware

from lebowski.actions import compute_stat_action
from lebowski.azure_connections import AKVConnector
from lebowski.db import DBHelper
from lebowski.router import route

TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('APP_ID')
CLIENT_SECRET = os.getenv('CLIENT_KEY')
ENV=os.getenv('ENV')

akv = AKVConnector(tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, env=ENV)

bot = Bot(token=akv.get_bot_token())
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(access_ids=akv.get_allowed_users()))
storage_account = TableService(connection_string=akv.get_storage_connection_string(), is_emulated=(ENV != "prod"))


@dp.message_handler(commands=['help'])
async def process_help(msg: types.Message):
    await msg.reply("""
Бот для учёта расходов на машину и прочее. Также напоминает о важных событиях, например что надо проверить двигатель
или что пора заменить паспорт.
Команды:
/help - эта подсказка
/reminders - выводит список всех напоминалок, с порядковыми номерами и указанием как скоро наступит событие
/stat - выводит пробег, стоимости, аналитику по стоимостям, временные характеристики
""")


@dp.message_handler(commands=['stat'])
async def process_stat(msg: types.Message):
    db = DBHelper(storage_account)
    try:
        datasets = db.get_stat_data(msg.from_user.id)
        results = compute_stat_action(datasets, akv)
        answer = text(
            text(emojize(":car:"), bold("Пробег:"),results['total_mileage'], "км"),
            text(emojize(":moneybag:"), bold("Траты"), numbers.format_currency(results['total_spending'], 'EUR')),
            text(emojize(":chart_with_upwards_trend:"), bold("Цена км:"), numbers.format_currency(results['total_spending'] / results['total_mileage'], 'EUR')),
            sep='\n'
        )
        await bot.send_message(msg.from_user.id, answer, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logging.error(e)
        await bot.send_message(msg.from_user.id, f"Received: {msg.text}, server error {str(e)}")    


@dp.message_handler(commands=['reminders'])
async def process_list_reminders(msg: types.Message):
    db = DBHelper(storage_account)
    try:
        reminders = db.list_reminders(msg.from_user.id)
        await bot.send_message(msg.from_user.id, f"Количество напоминалок: {len(reminders)}")
        for r in reminders:
            await bot.send_message(msg.from_user.id, r)
    except Exception as e:
        logging.error(e)
        await bot.send_message(msg.from_user.id, f"Received: {msg.text}, server error {str(e)}")    


@dp.message_handler()
async def process_message(msg: types.Message):
    try:
        (action, args) = route(msg.text)
        result = action(args, storage_account, msg.from_user.id, akv)
        await bot.send_message(msg.from_user.id, result)
    except Exception as e:
        logging.error(e)
        await bot.send_message(msg.from_user.id, f"Received: {msg.text}, server error {str(e)}")    

async def main(req: func.HttpRequest) -> func.HttpResponse:
    update = req.get_json()
    updateObj = types.Update.to_object(update)
    logging.info('Update: ' + str(updateObj))
    Bot.set_current(dp.bot)
    await dp.process_update(updateObj)
    return func.HttpResponse("", status_code=200) 
