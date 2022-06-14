from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import ration_callback, nutrition_by_type_callback, start_nutrition_callback, \
    nutrition_callback, meal_callback, subscribe_nutrition_callback, unsubscribe_nutrition_callback
from keyboards.inline.nutrition import nutrition_type_keyboard, nutritions_keyboard, nutrition_meal_keyboard, \
    nutrition_choose_keyboard
from loader import dp
from utils.db_api.database import Nutrition, NutritionMeal, UserToNotifyAboutNutritionMeal, User, Meal
from utils.nutrition.meal import get_next_and_prev_meal_id


@dp.callback_query_handler(ration_callback.filter())
async def bot_select_nutrition_type(call: CallbackQuery, callback_data: dict):
    await call.message.edit_text(text="Выбери тип питания:", reply_markup=nutrition_type_keyboard())


@dp.callback_query_handler(nutrition_by_type_callback.filter())
async def bot_nutrition_by_type(call: CallbackQuery, callback_data: dict):
    user = await User.get(User.id == call.from_user.id)
    nutritions = await Nutrition.filter(Nutrition.type == callback_data['type'], Nutrition.sex == user.sex)
    await call.message.edit_text(text="Выбери рацион из списка ниже:",
                                 reply_markup=nutritions_keyboard(nutritions=nutritions))


@dp.callback_query_handler(nutrition_callback.filter())
async def bot_nutrition(call: CallbackQuery, callback_data: dict):
    nutrition = await Nutrition.get(Nutrition.id == int(callback_data['id']))
    notification = await UserToNotifyAboutNutritionMeal.get(UserToNotifyAboutNutritionMeal.user_id == call.from_user.id,
                                                            UserToNotifyAboutNutritionMeal.nutrition_id == nutrition.id)

    await call.message.edit_text(
        text=f"🏋🏻‍♂️ {nutrition.name}\n\n👨🏻‍🏫 {nutrition.description}",
        reply_markup=nutrition_choose_keyboard(nutrition=nutrition, is_notifiable=bool(notification))
    )


@dp.callback_query_handler(start_nutrition_callback.filter())
async def bot_nutrition_start(call: CallbackQuery, callback_data: dict):
    nutrition = await Nutrition.get(Nutrition.id == int(callback_data['id']))
    meal = await NutritionMeal.get(NutritionMeal.nutrition_id == nutrition.id)
    await bot_nutrition_meal(call=call, callback_data={'id': meal.id})


@dp.callback_query_handler(meal_callback.filter())
async def bot_nutrition_meal(call: CallbackQuery, callback_data: dict):
    nutrition_meal = await NutritionMeal.get(NutritionMeal.id == int(callback_data['id']))
    prev_meal_id, next_meal_id = await get_next_and_prev_meal_id(current_meal=nutrition_meal)
    meals = await Meal.filter(Meal.nutrition_meal_id == nutrition_meal.id)
    meals_text = "\n\n".join([f"🍽 {meal.name}\n🔢 {meal.amount}" for meal in meals])

    await call.message.edit_text(
        text=f"⏲ {nutrition_meal.mealtime}\n\n{meals_text}",
        reply_markup=nutrition_meal_keyboard(
            nutrition_meal=nutrition_meal, prev_meal_id=prev_meal_id, next_meal_id=next_meal_id
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
