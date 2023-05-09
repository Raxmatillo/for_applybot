from aiogram import types

from loader import dp


# Echo bot
@dp.message_handler(state=None, content_types='any')
async def bot_echo(message: types.Message):
    await message.answer("Iltimos amalni bajaring, yoki /start buyrug'ini yuboring!")
