from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

ticket_type_cd = CallbackData("ticket_type", "id")




from loader import db


async def ticket_type_keyboards():
    markup = InlineKeyboardMarkup(row_width=1)

    ticket_types = await db.get_all_tickets()

    for ticket_type in ticket_types:
        button_name = f"{ticket_type['name']}"
        markup.insert(
            InlineKeyboardButton(
                text=button_name,
                callback_data=ticket_type_cd.new(id=ticket_type['id'])
            )
        )

    return markup
