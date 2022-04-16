from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import new_user_parameters_callback


def parameters_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Добавить актуальные параметры", callback_data=new_user_parameters_callback.new())
    )
    return keyboard
