from aiogram.dispatcher.filters.state import StatesGroup, State


class UserParametersState(StatesGroup):
    height = State()
    weight = State()



