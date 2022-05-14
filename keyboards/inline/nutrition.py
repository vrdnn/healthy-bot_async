from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import snack_callback, ration_callback


def nutrition_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Рацион питания", callback_data=ration_callback.new()),
        InlineKeyboardButton(text="Перекусы", callback_data=snack_callback.new())
    )
    return keyboard
