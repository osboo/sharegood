import os
import logging

import azure.functions as func
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from lebowski.connections_telegram import AKVConnector, TableStorageConnector
from middlewares.access import AccessMiddleware

TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('APP_ID')
CLIENT_SECRET = os.getenv('CLIENT_KEY')
AKV_URL = os.getenv('AKV_URL')

akv = AKVConnector(akv_url=AKV_URL, tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

bot = Bot(token=akv.get_bot_token())
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(access_ids=akv.get_allowed_users()))
storage_account = TableStorageConnector(akv.get_storage_connection_string())

@dp.message_handler()
async def echo_message(msg: types.Message):
    tables = [table.name for table in storage_account.table_service.list_tables()]
    await bot.send_message(msg.from_user.id, f"Echo: {msg.text} " + "".join(tables))

async def main(req: func.HttpRequest) -> func.HttpResponse:
    update = req.get_json()
    updateObj = types.Update.to_object(update)
    logging.info('Update: ' + str(updateObj))
    Bot.set_current(dp.bot)
    await dp.process_update(updateObj)
    return func.HttpResponse("", status_code=200) 
