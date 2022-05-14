from aiogram import types

from keyboards.default.menu import NUTRITION
from keyboards.inline.nutrition import nutrition_keyboard
from loader import dp


@dp.message_handler(text=NUTRITION, state='*')
async def bot_nutrition(message: types.Message):
    await message.answer("Что ты хочешь посмотреть?", reply_markup=nutrition_keyboard())
