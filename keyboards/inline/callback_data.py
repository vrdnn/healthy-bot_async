from aiogram.utils.callback_data import CallbackData

user_parameters_callback = CallbackData("user_parameters")
user_sex_callback = CallbackData("user_sex", "sex")

ration_callback = CallbackData("ration")

snack_callback = CallbackData("snack")
snack_add_callback = CallbackData("snack_add")

select_workout_type_callback = CallbackData("select_workout_type")
workout_by_type_callback = CallbackData("workout_type", "type")
workout_callback = CallbackData("workout", "id")
start_workout_callback = CallbackData("start_workout", "id")
iteration_callback = CallbackData("iteration", "id")
