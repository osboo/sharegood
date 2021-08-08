from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AccessMiddleware(BaseMiddleware):
    def __init__(self, access_ids: list):
        self.access_ids = access_ids
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        if str(message.from_user.id) not in self.access_ids:
            await message.answer(f"Access Denied. Consider asking bot owner to add your id to whitelist. Your id is {str(message.from_user.id)}")
            raise CancelHandler()
