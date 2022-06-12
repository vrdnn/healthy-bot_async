from collections import defaultdict
from typing import List

from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import ration_callback, nutrition_by_type_callback, start_nutrition_callback, \
    nutrition_callback, meal_callback, subscribe_nutrition_callback, unsubscribe_nutrition_callback
from keyboards.inline.nutrition import nutrition_type_keyboard, nutritions_keyboard, meal_keyboard, \
    nutrition_choose_keyboard
from loader import dp
from utils.db_api.database import Nutrition, NutritionMeal, UserToNotifyAboutNutritionMeal
from utils.nutrition.meal import get_next_and_prev_meal_id


@dp.callback_query_handler(ration_callback.filter())
async def bot_select_nutrition_type(call: CallbackQuery, callback_data: dict):
    await call.message.edit_text(text="Выбери тип питания:", reply_markup=nutrition_type_keyboard())


@dp.callback_query_handler(nutrition_by_type_callback.filter())
async def bot_nutrition_by_type(call: CallbackQuery, callback_data: dict):
    nutritions = await Nutrition.filter(Nutrition.type == callback_data['type'])
    await call.message.edit_text(text="Выбери рацион из списка ниже:",
                                 reply_markup=nutritions_keyboard(nutritions=nutritions))


@dp.callback_query_handler(nutrition_callback.filter())
async def bot_nutrition(call: CallbackQuery, callback_data: dict):
    nutrition = await Nutrition.get(Nutrition.id == int(callback_data['id']))
    notification = await UserToNotifyAboutNutritionMeal.get(UserToNotifyAboutNutritionMeal.user_id == call.from_user.id,
                                                            UserToNotifyAboutNutritionMeal.nutrition_id == nutrition.id)
    meals: List[NutritionMeal] = await NutritionMeal.filter(NutritionMeal.nutrition_id == nutrition.id)

    meal_type_to_name = defaultdict(list)
    for meal in meals:
        meal_type_to_name[meal.mealtime].append(f'• {meal.name}')

    meals_text = ""
    for key, value in meal_type_to_name.items():
        meals_text += f"{key}:\n" + "\n".join(value) + "\n\n"

    await call.message.edit_text(
        text=f"🏋🏻‍♂️ {nutrition.name}\n\n👨🏻‍🏫 {nutrition.description}\n\n{meals_text}",
        reply_markup=nutrition_choose_keyboard(nutrition=nutrition, is_notifiable=bool(notification))
    )


@dp.callback_query_handler(start_nutrition_callback.filter())
async def bot_nutrition_start(call: CallbackQuery, callback_data: dict):
    nutrition = await Nutrition.get(Nutrition.id == int(callback_data['id']))
    meal = await NutritionMeal.get(NutritionMeal.nutrition_id == nutrition.id)
    await bot_nutrition_meal(call=call, callback_data={'id': meal.id})


@dp.callback_query_handler(meal_callback.filter())
async def bot_nutrition_meal(call: CallbackQuery, callback_data: dict):
    meal = await NutritionMeal.get(NutritionMeal.id == int(callback_data['id']))
    prev_meal_id, next_meal_id = await get_next_and_prev_meal_id(current_meal=meal)
    await call.message.edit_text(
        text=f"⏲ {meal.mealtime}\n\n🍽 {meal.name}\n\n🔢 {meal.amount}",
        reply_markup=meal_keyboard(
            meal=meal, prev_meal_id=prev_meal_id, next_meal_id=next_meal_id
        )
    )


@dp.callback_query_handler(subscribe_nutrition_callback.filter())
async def bot_subscribe_nutrition(call: CallbackQuery, callback_data: dict):
    nutrition = await Nutrition.get(Nutrition.id == int(callback_data['id']))
    await UserToNotifyAboutNutritionMeal.create(nutrition_id=nutrition.id, user_id=call.from_user.id)
    await call.answer("🔔 Уведомления включены")
    await bot_nutrition(call=call, callback_data=callback_data)


@dp.callback_query_handler(unsubscribe_nutrition_callback.filter())
async def bot_unsubscribe_nutrition(call: CallbackQuery, callback_data: dict):
    nutrition = await Nutrition.get(Nutrition.id == int(callback_data['id']))
    notification = await UserToNotifyAboutNutritionMeal.get(
        UserToNotifyAboutNutritionMeal.nutrition_id == nutrition.id,
        UserToNotifyAboutNutritionMeal.user_id == call.from_user.id
    )
    if notification:
        await notification.delete()
        await call.answer("🔕 Уведомления отключены")
    await bot_nutrition(call=call, callback_data=callback_data)
