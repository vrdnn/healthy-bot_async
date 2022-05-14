from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.menu import ABOUT_USER
from keyboards.inline.callback_data import user_parameters_callback
from keyboards.inline.parameters import parameters_keyboard
from loader import dp
from states.parameters import UserParametersState
from utils.db_api.database import UserParametersPerDay


@dp.message_handler(commands=['parameters'], state='*')
@dp.message_handler(text=ABOUT_USER, state='*')
async def bot_parameters(message: types.Message):
    last_parameters = await UserParametersPerDay.query.where(
        UserParametersPerDay.user_id == message.from_user.id).order_by(UserParametersPerDay.id.desc()).gino.first()

    if last_parameters:
        await message.answer(
            "\n".join(
                [
                    f"Последняя запись от {last_parameters.created_at.strftime('%d.%m.%Y %H:%M')}",
                    f"Рост: {last_parameters.height}",
                    f"Вес: {last_parameters.weight}",
                ]
            ),
            reply_markup=parameters_keyboard()
        )
    else:
        await UserParametersState.height.set()
        await message.answer("Пришли мне свой рост, чтобы я его записал!")


@dp.callback_query_handler(user_parameters_callback.filter(), state='*')
async def bot_new_user_parameters_callback(call: CallbackQuery, callback_data: dict):
    await UserParametersState.height.set()
    await call.message.answer("Пришли мне свой рост, чтобы я его записал!")


@dp.message_handler(content_types=['text'], state=UserParametersState.height)
async def bot_parameters_height(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 30 < int(message.text) < 250:
        await state.update_data(height=message.text)
        await UserParametersState.weight.set()
        await message.answer("Пришли мне свой вес и я его запишу!")
    else:
        await message.answer("Некорректные данные, попробуйте снова!")


@dp.message_handler(content_types=['text'], state=UserParametersState.weight)
async def bot_parameters_weight(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 10 < int(message.text) < 300:
        await state.update_data(weight=message.text)
        data = await state.get_data()
        await state.reset_state(with_data=True)

        await UserParametersPerDay.create(user_id=message.from_user.id, height=int(data['height']),
                                          weight=int(data['weight']))

        await message.answer(f"Отлично, записал!\n\nРост: {data['height']}\nВес: {data['weight']}")
    else:
        await message.answer("Некорректные данные, попробуйте снова!")
