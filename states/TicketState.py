from aiogram.dispatcher.filters.state import State, StatesGroup

class Ticket(StatesGroup):
    full_name = State()
    group_number = State()
    faculty = State()
    file = State()
    confirm = State()

