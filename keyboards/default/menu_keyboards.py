from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ariza"),
            KeyboardButton("Info")
        ]
    ], resize_keyboard=True
)