from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: types.Message):
    text = (
        "Список команд: ",
        "/start - Начать диалог",
        "/help - Получить справку",
        "/parameters - Заполнить параметры на сегодня",
        "/cancel - Отменить действие",
    )

    await message.answer("\n".join(text))
