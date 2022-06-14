from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.default.menu import WORKOUTS
from keyboards.inline.callback_data import workout_by_type_callback, select_workout_type_callback, workout_callback, \
    start_workout_callback, iteration_callback
from keyboards.inline.workout import workout_type_keyboard, workouts_keyboard, workout_keyboard, iteration_keyboard
from loader import dp
from utils.db_api.database import Workout, WorkoutIteration, Exercise, User
from utils.workout.exercise import get_next_and_prev_iteration_id


@dp.message_handler(text=WORKOUTS, state='*')
@dp.message_handler(commands=['workout'], state='*')
async def bot_workout_type(message: types.Message):
    await message.answer(text="Выбери тип тренировки:", reply_markup=workout_type_keyboard())


@dp.callback_query_handler(select_workout_type_callback.filter())
async def bot_select_workout_type(call: CallbackQuery, callback_data: dict):
    await call.message.edit_text(text="Выбери тип тренировки:", reply_markup=workout_type_keyboard())


@dp.callback_query_handler(workout_by_type_callback.filter())
async def bot_workouts_by_type(call: CallbackQuery, callback_data: dict):
    user = await User.get(User.id == call.from_user.id)
    workouts = await Workout.filter(Workout.type == callback_data['type'], Workout.sex == user.sex)
    await call.message.edit_text(text="Выбери тренировку из списка ниже:",
                                 reply_markup=workouts_keyboard(workouts=workouts))


@dp.callback_query_handler(workout_callback.filter())
async def bot_workout(call: CallbackQuery, callback_data: dict):
    workout = await Workout.get(Workout.id == int(callback_data['id']))
    exercise_ids = [exercise_id[0] for exercise_id in await WorkoutIteration.filter(
        WorkoutIteration.workout_id == workout.id, select_values=['exercise_id']
    )]
    exercise_names = [name[0] for name in await Exercise.filter(Exercise.id.in_(exercise_ids), select_values=['name'])]
    exercises_text = "\n".join([f"{index + 1}. {value}" for index, value in enumerate(exercise_names)])
    await call.message.edit_text(
        text=f"🏋🏻‍♂️ {workout.name}\n\n👨🏻‍🏫 {workout.description}\n\n🥊 Упражнения:\n{exercises_text}",
        reply_markup=workout_keyboard(workout=workout)
    )


@dp.callback_query_handler(start_workout_callback.filter())
async def bot_workout_start(call: CallbackQuery, callback_data: dict):
    workout = await Workout.get(Workout.id == int(callback_data['id']))
    iteration = await WorkoutIteration.get(WorkoutIteration.workout_id == workout.id)
    await bot_workout_iteration(call=call, callback_data={'id': iteration.id})


@dp.callback_query_handler(iteration_callback.filter())
async def bot_workout_iteration(call: CallbackQuery, callback_data: dict):
    iteration = await WorkoutIteration.get(WorkoutIteration.id == int(callback_data['id']))
    exercise = await Exercise.get(Exercise.id == iteration.exercise_id)
    prev_iteration_id, next_iteration_id = await get_next_and_prev_iteration_id(current_iteration=iteration)
    exercise_name = f"<a href='{exercise.image}'>{exercise.name}</a>" if exercise.image else exercise.name
    await call.message.edit_text(
        text=f"🏋🏻‍♂️ {exercise_name}\n\n👨🏻‍🏫 {exercise.description}\n\n🔢 {iteration.amount}",
        reply_markup=iteration_keyboard(
            iteration=iteration, prev_iteration_id=prev_iteration_id, next_iteration_id=next_iteration_id
        )
    )
