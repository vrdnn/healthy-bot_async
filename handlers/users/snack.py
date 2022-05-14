from datetime import date
from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.constants import calories_for_product
from keyboards.inline.callback_data import snack_add_callback, snack_callback
from keyboards.inline.snack import snack_keyboard
from loader import dp
from states.snack import SnackAddState
from utils.db_api.database import UserCaloriesPerDay
from utils.nutrition.calculate import calculate_calories_for_product


@dp.message_handler(commands=['nutrition'], state='*')
async def bot_snack(message: types.Message):
    date_obj = date.today()
    snacks: List[UserCaloriesPerDay] = await UserCaloriesPerDay.for_day(user_id=message.from_user.id, date_obj=date_obj)
    text = f"📆 {date_obj.strftime('%d.%m.%Y')}\n\n"
    sum_calories = 0

    for snack in snacks:
        text += f"⏱ {snack.created_at.strftime('%H:%M')}\nПродукт: {snack.product}\nКалории: {snack.quantity}\nГраммы: {snack.gram}\n\n"
        sum_calories += snack.quantity

    if sum_calories:
        text += f"Всего калорий за день: {sum_calories}"

    if not snacks:
        text += "Сегодня еще не было перекусов."

    await message.answer(text=text, reply_markup=snack_keyboard())


@dp.callback_query_handler(snack_callback.filter())
async def bot_snack_callback(call: CallbackQuery, callback_data: dict):
    date_obj = date.today()
    snacks: List[UserCaloriesPerDay] = await UserCaloriesPerDay.for_day(user_id=call.from_user.id, date_obj=date_obj)
    text = f"📆 {date_obj.strftime('%d.%m.%Y')}\n\n"
    sum_calories = 0

    for snack in snacks:
        text += f"⏱ {snack.created_at.strftime('%H:%M')}\nПродукт: {snack.product}\nКалории: {snack.quantity}\nГраммы: {snack.gram}\n\n"
        sum_calories += snack.quantity

    if sum_calories:
        text += f"Всего калорий за день: {sum_calories}"

    if not snacks:
        text += "Сегодня еще не было перекусов."

    await call.message.answer(text=text, reply_markup=snack_keyboard())


@dp.callback_query_handler(snack_add_callback.filter())
async def bot_add_snack(call: CallbackQuery, callback_data: dict):
    await call.message.answer(text="Пришли название продукта")
    await SnackAddState.product.set()


@dp.message_handler(content_types=['text'], state=SnackAddState.product)
async def bot_add_snack_product(message: types.Message, state: FSMContext):
    await state.update_data(product=message.text)
    await message.answer(text="Пришли количество грамм")
    await SnackAddState.gram.set()


@dp.message_handler(content_types=['text'], state=SnackAddState.gram)
async def bot_add_snack_gram(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(gram=message.text)
        data = await state.get_data()

        calories = calculate_calories_for_product(product=data['product'], gram=int(data['gram']))
        if calories:
            await message.answer(text=f"Пришли количество калорий (~<code>{int(calories)}</code> ккал.)")
        else:
            await message.answer(text="Пришли количество калорий")
        await SnackAddState.quantity.set()
    else:
        await message.answer("Некорректные данные, попробуй еще раз")


@dp.message_handler(content_types=['text'], state=SnackAddState.quantity)
async def bot_add_snack_quantity(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(quantity=message.text)

        data = await state.get_data()
        await UserCaloriesPerDay.create(user_id=message.from_user.id, product=data['product'], gram=int(data['gram']),
                                        quantity=int(data['quantity']))

        await message.answer(text="Добавлено")
        await state.reset_state(with_data=True)

        await bot_snack(message)
    else:
        await message.answer("Некорректные данные, попробуй еще раз")
