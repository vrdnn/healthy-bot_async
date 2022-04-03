from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from states.start import UserStartState
from utils.db_api.database import User, UserParametersPerDay


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await User.get_or_create(
        id=message.from_user.id, first_name=message.from_user.first_name, username=message.from_user.username
    )
    await message.answer(f"Привет, {message.from_user.full_name}! Давай заполним твои параметры. Пришли мне свой рост")
    await UserStartState.height.set()


@dp.message_handler(content_types=['text'], state=UserStartState.height)
async def bot_set_height(message: types.Message, state: FSMContext):
    await message.answer(f"Теперь пришли мне вес")
    await state.update_data(height=message.text)
    await UserStartState.weight.set()


@dp.message_handler(content_types=['text'], state=UserStartState.weight)
async def bot_set_weight(message: types.Message, state: FSMContext):
    await message.answer(f"Отлично, я записал твои данные!")
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await state.reset_state(with_data=True)
    await UserParametersPerDay.create(user_id=message.from_user.id, height=int(data['height']),
                                      weight=int(data['weight']))
