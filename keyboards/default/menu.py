from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

NUTRITION = "🥑 Питание"
WORKOUTS = "💪 Тренировки"
CAL_CALCULATOR = "🥦 Калькулятор калорий"
ABOUT_USER = "📜 Информация о себе"

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(NUTRITION),
            KeyboardButton(WORKOUTS),
        ],
        [
            KeyboardButton(CAL_CALCULATOR),
            KeyboardButton(ABOUT_USER)
        ],
    ], resize_keyboard=True
)
