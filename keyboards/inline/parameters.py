from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import user_parameters_callback, user_sex_callback


def parameters_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Добавить актуальные параметры", callback_data=user_parameters_callback.new())
    )
    return keyboard


def parameters_sex_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="👨", callback_data=user_sex_callback.new(sex='man')),
        InlineKeyboardButton(text="👩", callback_data=user_sex_callback.new(sex='woman'))
    )
    return keyboard
