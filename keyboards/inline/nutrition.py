from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import snack_callback, ration_callback, nutrition_by_type_callback, \
    nutrition_callback, start_nutrition_callback, meal_callback, \
    subscribe_nutrition_callback, unsubscribe_nutrition_callback
from utils.db_api.constants import NUTRITION_TYPE
from utils.db_api.database import Nutrition, NutritionMeal


def nutrition_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Рацион питания", callback_data=ration_callback.new()),
        InlineKeyboardButton(text="Перекусы", callback_data=snack_callback.new())
    )
    return keyboard


def nutrition_type_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        *[
            InlineKeyboardButton(text=button_text, callback_data=nutrition_by_type_callback.new(type=button_text))
            for button_text in NUTRITION_TYPE.keys()
        ]
    )
    return keyboard


def nutritions_keyboard(nutritions: List[Nutrition]):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        *[
            InlineKeyboardButton(text=nutrition.name, callback_data=nutrition_callback.new(id=nutrition.id))
            for nutrition in nutritions
        ]
    )
    keyboard.add(InlineKeyboardButton(text="🔙", callback_data=ration_callback.new()))
    return keyboard


def nutrition_choose_keyboard(nutrition: Nutrition, is_notifiable: bool):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        InlineKeyboardButton(text="🔙", callback_data=nutrition_by_type_callback.new(type=nutrition.type)),
        InlineKeyboardButton(text="🏃🏻‍♂️", callback_data=start_nutrition_callback.new(id=nutrition.id)),
    )
    if is_notifiable:
        keyboard.add(InlineKeyboardButton(text="🔕 Отключить уведомления",
                                          callback_data=unsubscribe_nutrition_callback.new(id=nutrition.id)))

    else:
        keyboard.add(InlineKeyboardButton(text="🔔 Включить уведомления",
                                          callback_data=subscribe_nutrition_callback.new(id=nutrition.id)))

    return keyboard


def nutrition_meal_keyboard(nutrition_meal: NutritionMeal, prev_meal_id: int, next_meal_id: int):
    keyboard = InlineKeyboardMarkup(row_width=2)
    if prev_meal_id is not None:
        keyboard.add(
            InlineKeyboardButton(text="🔙", callback_data=meal_callback.new(id=prev_meal_id)),
        )
    else:
        keyboard.add(
            InlineKeyboardButton(text="🔙", callback_data=nutrition_callback.new(id=nutrition_meal.nutrition_id))
        )
    if next_meal_id is not None:
        keyboard.insert(
            InlineKeyboardButton(text="🔜", callback_data=meal_callback.new(id=next_meal_id)),
        )
    else:
        keyboard.insert(
            InlineKeyboardButton(text="🏁", callback_data=nutrition_callback.new(id=nutrition_meal.nutrition_id))
        )
    return keyboard
