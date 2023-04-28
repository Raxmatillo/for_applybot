from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

faculty_cd = CallbackData("faculty", "faculty_name")
confirm_cd = CallbackData("confirm", "confirm")

async def faculty_keyboards():
    markup = InlineKeyboardMarkup(row_width=2)
    faculties = await db.get__all_faculties()
    for faculty in faculties:
        button_text = f"{faculty['name']}"
        callback_data = faculty_cd.new(faculty_name=faculty['name'])
        markup.insert(
            InlineKeyboardButton(
                text=button_text, callback_data=callback_data
            )
        )
    return markup




confirmation_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Tasdiqlash",
                callback_data=confirm_cd.new(confirm="confirm")
            ),
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data=confirm_cd.new(confirm="unconfirm")
            )
        ]
    ], row_width=2
)