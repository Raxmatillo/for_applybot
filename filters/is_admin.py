from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import BoundFilter

from data.config import ADMINS


class AdminFilter(BoundFilter):
    async def check(self, message: Message):
        return str(message.from_user.id) in str(ADMINS)