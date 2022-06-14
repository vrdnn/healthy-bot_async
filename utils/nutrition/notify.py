import asyncio
import logging
from datetime import datetime

from data.config import TIME_BETWEEN_NOTIFICATION_UPDATES
from keyboards.inline.nutrition import nutrition_meal_keyboard
from loader import tz, bot
from utils.db_api.database import UserToNotifyAboutNutritionMeal, NutritionMeal, Meal
from utils.nutrition.meal import get_next_and_prev_meal_id

logger = logging.getLogger(__name__)


async def notify_users(time_between_notification_updates: int = TIME_BETWEEN_NOTIFICATION_UPDATES):
    while True:
        now = datetime.now(tz=tz)
        now_time = now.time().replace(second=0, microsecond=0)

        notifications = await UserToNotifyAboutNutritionMeal.all()
        nutrition_ids = set([notification.nutrition_id for notification in notifications])

        nutrition_meals = await NutritionMeal.filter(NutritionMeal.nutrition_id.in_(nutrition_ids),
                                                     NutritionMeal.time == now_time)

        for nutrition_meal in nutrition_meals:
            nutrition_id = nutrition_meal.nutrition_id

            prev_meal_id, next_meal_id = await get_next_and_prev_meal_id(current_meal=nutrition_meal)
            keyboard = nutrition_meal_keyboard(nutrition_meal=nutrition_meal, prev_meal_id=prev_meal_id,
                                               next_meal_id=next_meal_id)
            meals = await Meal.filter(Meal.nutrition_meal_id == nutrition_meal.id)
            meals_text = "\n\n".join([f"🍽 {meal.name}\n🔢 {meal.amount}" for meal in meals])

            for user_id in [notification.user_id for notification in notifications if
                            notification.nutrition_id == nutrition_id]:
                try:
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"⏲ {nutrition_meal.mealtime}\n\n{meals_text}",
                        reply_markup=keyboard
                    )
                except:
                    logger.error(f"Can not send notification to user with user_id={user_id}")

        await asyncio.sleep(time_between_notification_updates)
