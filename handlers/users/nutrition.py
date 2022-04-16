from datetime import date

from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.default.menu import NUTRITION
from keyboards.inline.callback_data import lunch_nutrition_callback
from keyboards.inline.ration import nutrition_keyboard
from loader import dp
from utils.db_api.database import UserCaloriesPerDay

now = date.today()


@dp.message_handler(text=NUTRITION, state='*')
async def bot_nutrition(message: types.Message):
    today_ration = await UserCaloriesPerDay.for_day(date.today())

    await message.answer(
        "\n".join(
            [
                f"Рацион на {now.strftime('%d.%m.%Y')}",
                f"Завтрак: ",
                f"Йогурт – 100г.",
                f"Геркулес – 50г.",
                f"Творог 9% – 100г",
            ]
        ),
        reply_markup=nutrition_keyboard()
    )


@dp.callback_query_handler(lunch_nutrition_callback.filter(), state='*')
async def bot_breakfast_nutrition_callback(call: CallbackQuery, callback_data: dict):
    await call.message.answer("Lunch", reply_markup=nutrition_keyboard())

