from aiogram.dispatcher.filters.state import StatesGroup, State


class SnackAddState(StatesGroup):
    product = State()
    quantity = State()
    gram = State()
