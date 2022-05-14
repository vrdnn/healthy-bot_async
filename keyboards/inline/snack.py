from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import snack_add_callback


def snack_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Добавить перекус", callback_data=snack_add_callback.new())
    )
    return keyboard
