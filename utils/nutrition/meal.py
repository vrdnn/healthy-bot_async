from utils.db_api.database import NutritionMeal


async def get_next_and_prev_meal_id(current_meal: NutritionMeal):
    meal_ids = [meal_id[0] for meal_id in
                await NutritionMeal.filter(
                    NutritionMeal.nutrition_id == current_meal.nutrition_id, select_values=['id']
                )]
    prev_meals = [meal_id for meal_id in meal_ids if meal_id < current_meal.id]
    prev_meal_id = prev_meals[-1] if prev_meals else None

    next_meals = [meal_id for meal_id in meal_ids if meal_id > current_meal.id]
    next_meal_id = next_meals[0] if next_meals else None

    return prev_meal_id, next_meal_id
