from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import workout_by_type_callback, workout_callback, select_workout_type_callback, \
    start_workout_callback, iteration_callback
from utils.db_api.constants import WORKOUT_TYPE
from utils.db_api.database import Workout, WorkoutIteration


def workout_type_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        *[
            InlineKeyboardButton(text=button_text, callback_data=workout_by_type_callback.new(type=button_text))
            for button_text in WORKOUT_TYPE.keys()
        ]
    )
    return keyboard


def workouts_keyboard(workouts: List[Workout]):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        *[
            InlineKeyboardButton(text=workout.name, callback_data=workout_callback.new(id=workout.id))
            for workout in workouts
        ]
    )
    keyboard.add(InlineKeyboardButton(text="🔙", callback_data=select_workout_type_callback.new()))
    return keyboard


def workout_keyboard(workout: Workout):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        InlineKeyboardButton(text="🔙", callback_data=workout_by_type_callback.new(type=workout.type)),
        InlineKeyboardButton(text="🏃🏻‍♂️", callback_data=start_workout_callback.new(id=workout.id)),
    )
    return keyboard


def iteration_keyboard(iteration: WorkoutIteration, prev_iteration_id: int, next_iteration_id: int):
    keyboard = InlineKeyboardMarkup(row_width=2)
    if prev_iteration_id is not None:
        keyboard.add(
            InlineKeyboardButton(text="🔙", callback_data=iteration_callback.new(id=prev_iteration_id)),
        )
    else:
        keyboard.add(
            InlineKeyboardButton(text="🔙", callback_data=workout_callback.new(id=iteration.workout_id))
        )
    if next_iteration_id is not None:
        keyboard.insert(
            InlineKeyboardButton(text="🔜", callback_data=iteration_callback.new(id=next_iteration_id)),
        )
    else:
        keyboard.insert(
            InlineKeyboardButton(text="🏁", callback_data=workout_callback.new(id=iteration.workout_id))
        )
    return keyboard
