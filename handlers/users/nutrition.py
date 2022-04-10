from datetime import date
from aiogram import types
from sqlalchemy import and_

from keyboards.default.menu import NUTRITION
from loader import dp
from utils.db_api.database import UserCaloriesPerDay

now = date.today()


@dp.message_handler(text=NUTRITION, state='*')
async def bot_nutrition(message: types.Message):
    today_ration = await UserCaloriesPerDay.for_day(date.today())

    await message.answer(
        "\n".join(
            [
                now.strftime("%d.%m.%Y")
            ]
        )
    )


