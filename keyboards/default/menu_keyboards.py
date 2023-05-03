from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("📝 Ariza"),
            KeyboardButton("ℹ️ Info")
        ]
    ], resize_keyboard=True
)


registration_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🌐 Ro'yxatdan o'tish")
        ]
    ], resize_keyboard=True
)