from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.menu_keyboards import menu, registration_keyboard
from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await db.get_user(telegram_id=message.from_user.id)
    if user == None:
        await message.answer(f"Assalomu alaykum "
                             f"{message.from_user.full_name}\n\n @shermuhammadovfardu kanaliga obuna bo'ling!",
                             reply_markup=registration_keyboard)
    else:
        await message.answer("Quyidagi menyulardan birini tanlang",
                             reply_markup=menu)