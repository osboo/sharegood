import asyncio
import json
import logging

import azure.functions as func
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

TOKEN = "563468769:AAGwT-eH4Td8aE56we0ZUTa-bkh0_21FU5o"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Start message handler")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Simple echo: return whatever is coming")

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

# async def temp():
#     s = """{"update_id": 40124897, "message": {"message_id": 22, "from": {"id": 229598673, "is_bot": false, "first_name": "Os", "username": "oooobso", "language_code": "en"}, "chat": {"id": 229598673, "first_name": "Os", "username": "oooobso", "type": "private"}, "date": 1623009694, "text": "yyy"}}"""
#     x = types.Update.to_object(json.loads(s))
#     print(x)
#     await dp.process_update(x)

# if __name__ == '__main__':
#     asyncio.get_event_loop().run_until_complete( temp() )
