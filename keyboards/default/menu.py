from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

NUTRITION = "🥑 Питание"
WORKOUTS = "💪 Тренировки"
ABOUT_USER = "📜 Информация о себе"

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(NUTRITION)],
        [KeyboardButton(WORKOUTS)],
        [KeyboardButton(ABOUT_USER)]
    ], resize_keyboard=True
)
