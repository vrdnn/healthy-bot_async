from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from keyboards.default import menu
from keyboards.inline.callback_data import user_sex_callback
from keyboards.inline.parameters import parameters_sex_keyboard
from loader import dp
from states.parameters import UserParametersState
from utils.db_api.database import User, UserParametersPerDay


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await User.get_or_create(
        id=message.from_user.id, first_name=message.from_user.first_name, username=message.from_user.username
    )
    await message.answer(f"Привет, {message.from_user.full_name}! Я твой бот-помощник для поддержания здорового "
                         f"образа жизни. Для начала давай заполним информацию о тебе. Укажи свой пол:",
                         reply_markup=parameters_sex_keyboard())


@dp.callback_query_handler(user_sex_callback.filter())
async def bot_set_sex(call: CallbackQuery, callback_data: dict):
    user = await User.get(id=call.from_user.id)
    await user.update(sex=callback_data['sex']).apply()

    await call.message.answer(f"Теперь пришли мне рост", reply_markup=menu)
    await UserParametersState.height.set()


@dp.message_handler(content_types=['text'], state=UserParametersState.height)
async def bot_set_height(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer(f"Теперь пришли мне вес", reply_markup=menu)
        await state.update_data(height=message.text)
        await UserParametersState.weight.set()
    else:
        await message.answer("Некорректные данные, попробуй еще раз")


@dp.message_handler(content_types=['text'], state=UserParametersState.weight)
async def bot_set_weight(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer(f"Отлично, я записал твои данные!")
        await state.update_data(weight=message.text)
        data = await state.get_data()
        await state.reset_state(with_data=True)
        await UserParametersPerDay.create(user_id=message.from_user.id, height=int(data['height']),
                                          weight=int(data['weight']))
    else:
        await message.answer("Некорректные данные, попробуй еще раз")
