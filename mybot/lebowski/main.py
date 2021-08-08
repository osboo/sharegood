import os
import logging

import azure.functions as func
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from lebowski.connections_telegram import get_azure_ad_token, get_bot_token, get_allowed_users
from middlewares.access import AccessMiddleware

TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('APP_ID')
CLIENT_SECRET = os.getenv('CLIENT_KEY')

ad_token = get_azure_ad_token(tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

bot = Bot(token=get_bot_token(azure_ad_token=ad_token))
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(access_ids=get_allowed_users(azure_ad_token=ad_token)))

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, f"Echo: {msg.text}")

async def main(req: func.HttpRequest) -> func.HttpResponse:
    update = req.get_json()
    updateObj = types.Update.to_object(update)
    logging.info('Update: ' + str(updateObj))
    Bot.set_current(dp.bot)
    await dp.process_update(updateObj)
    return func.HttpResponse("", status_code=200) 
