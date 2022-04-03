from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Питание"),
            KeyboardButton(text="Тренировки"),
        ],
        [
            KeyboardButton(text="Калькулятор калорий"),
            KeyboardButton(text="Информация о себе")
        ],
    ]
)
