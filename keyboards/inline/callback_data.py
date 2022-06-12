from aiogram.utils.callback_data import CallbackData

user_parameters_callback = CallbackData("user_parameters")
user_sex_callback = CallbackData("user_sex", "sex")

ration_callback = CallbackData("ration")

snack_callback = CallbackData("snack")
snack_add_callback = CallbackData("snack_add")

select_workout_type_callback = CallbackData("select_workout_type")
select_nutrition_type_callback = CallbackData("select_nutrition_type")
workout_by_type_callback = CallbackData("workout_type", "type")
nutrition_by_type_callback = CallbackData("nutrition_type", "type")
subscribe_nutrition_callback = CallbackData("subscribe_nutrition", "id")
unsubscribe_nutrition_callback = CallbackData("unsubscribe_nutrition", "id")
workout_callback = CallbackData("workout", "id")
nutrition_callback = CallbackData("nutrition", "id")
start_workout_callback = CallbackData("start_workout", "id")
start_nutrition_callback = CallbackData("start_nutrition", "id")
iteration_callback = CallbackData("iteration", "id")
meal_callback = CallbackData("meal", "id")
