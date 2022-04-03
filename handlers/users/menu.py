from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message
from keyboards.default import menu
from loader import dp


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выбери один из пунктов меню", reply_markup=menu)


@dp.message_handler(Text(equals=["Питание", "Тренировки", "Калькулятор калорий", "Информация о себе"]))
async def get_key(message: Message):
    await message.answer(f"Ты выбрал {message.text}. Спасибо")
