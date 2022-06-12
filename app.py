import asyncio

from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.db_api.database import create_database
from utils.notify_admins import on_startup_notify
from utils.nutrition.notify import notify_users
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_database())

    loop.create_task(notify_users())

    executor.start_polling(dp, on_startup=on_startup)
