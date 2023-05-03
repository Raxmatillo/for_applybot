from aiogram.dispatcher.filters.state import State, StatesGroup

class User(StatesGroup):
    faculty = State()
    group_number = State()
    full_name = State()
    phone_number = State()

class Ticket(StatesGroup):
    tickey_type = State()
    file = State()
    text = State()
    confirm = State()

