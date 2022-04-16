from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import lunch_nutrition_callback, \
    dinner_nutrition_callback


def nutrition_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Обед", callback_data=lunch_nutrition_callback.new()),
        InlineKeyboardButton(text="Ужин", callback_data=dinner_nutrition_callback.new())
    )
    return keyboard
