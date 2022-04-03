from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStartState(StatesGroup):
    height = State()
    weight = State()
