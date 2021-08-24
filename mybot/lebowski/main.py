import os
import logging

import azure.functions as func
from azure.storage.table import TableService
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from lebowski.azure_connections import AKVConnector
from lebowski.router import route
from middlewares.access import AccessMiddleware

TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('APP_ID')
CLIENT_SECRET = os.getenv('CLIENT_KEY')
ENV=os.getenv('ENV')

akv = AKVConnector(tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, env=ENV)

bot = Bot(token=akv.get_bot_token())
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(access_ids=akv.get_allowed_users()))
storage_account = TableService(connection_string=akv.get_storage_connection_string(), is_emulated=(ENV != "prod"))


@dp.message_handler()
async def echo_message(msg: types.Message):
    try:
        (action, args) = route(msg.text)
        action(args, storage_account, msg.from_user.id)
        await bot.send_message(msg.from_user.id, f"Received: {msg.text}")
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
