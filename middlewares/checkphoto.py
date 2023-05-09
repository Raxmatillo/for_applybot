import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import bot


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            if update.message.media_group_id:
                await update.message.answer("❗️ Iltimos, 1 dona rasm yuboring!")
                raise CancelHandler()



            # raise CancelHandler()