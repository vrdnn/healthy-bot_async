from __future__ import annotations

from datetime import date, timedelta

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.exceptions import BotBlocked
from gino import Gino
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import String, Index, Sequence, sql, DateTime, func, and_, Time
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base

from data.config import DATABASE_URL
from .constants import MAN, WOMAN, WORKOUT_TYPE, NUTRITION_TYPE
from .types import ChoiceType

Base = declarative_base()

database = Gino()


class BaseModel(database.Model):
    query: sql.Select

    @classmethod
    async def get(cls, *args, select_values: list | tuple = ()):
        if select_values:
            return await cls.select(*select_values).where(and_(*args)).order_by("id").gino.first()
        return await cls.query.where(and_(*args)).order_by("id").gino.first()

    @classmethod
    async def filter(cls, *args, select_values: list | tuple = ()):
        if select_values:
            return await cls.select(*select_values).where(and_(*args)).order_by("id").gino.all()
        return await cls.query.where(and_(*args)).order_by("id").gino.all()

    @classmethod
    async def all(cls):
        return await cls.query.gino.all()

    @classmethod
    async def count(cls) -> int:
        return await database.func.count(cls.id).gino.scalar()


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    first_name = Column(String(128))
    username = Column(String(128))
    sex = Column(ChoiceType({MAN: MAN, WOMAN: WOMAN}), nullable=True)

    _idx = Index('user_id_index', 'id')

    @classmethod
    async def get_by_id_or_create(cls, id: int, **kwargs):
        obj = await cls.get(cls.id == id)
        if not obj:
            obj = await cls.create(id=id, **kwargs)
        return obj

    @staticmethod
    async def mailing(bot: Bot, text: str, keyboard: InlineKeyboardMarkup = None) -> int:
        count_users = 0
        for user in await User.query.gino.all():
            try:
                await bot.send_message(chat_id=user.id, text=text, reply_markup=keyboard)
                count_users += 1
            except BotBlocked:
                pass
        return count_users


class UserParametersPerDay(BaseModel):
    __tablename__ = 'user_parameters_per_days'

    id = Column(Integer, Sequence('user_parameters_per_day_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    height = Column(Integer)
    weight = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

    _idx = Index('user_parameters_per_day_id_index', 'id')


class UserCaloriesPerDay(BaseModel):
    __tablename__ = 'user_calories_per_days'

    id = Column(Integer, Sequence('user_calories_per_day_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    quantity = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    gram = Column(Integer)
    product = Column(String(128))

    _idx = Index('user_calories_per_days_id_index', 'id')

    @classmethod
    async def for_day(cls, user_id: int, date_obj: date):
        return await cls.query.where(and_(cls.created_at >= date_obj, cls.created_at < date_obj + timedelta(1),
                                          cls.user_id == user_id)).gino.all()


class Exercise(BaseModel):
    __tablename__ = 'exercises'

    id = Column(Integer, Sequence('exercise_id_seq'), primary_key=True)
    name = Column(String(32))
    description = Column(String(256))
    image = Column(String(256))

    _idx = Index('exercise_id_index', 'id')


class WorkoutIteration(BaseModel):
    __tablename__ = 'workout_iterations'

    id = Column(Integer, Sequence('workout_iteration_id_seq'), primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    amount = Column(String())

    _idx = Index('workout_iteration_id_index', 'id')


class Workout(BaseModel):
    __tablename__ = 'workouts'

    id = Column(Integer, Sequence('workout_id_seq'), primary_key=True)
    name = Column(String(32))
    description = Column(String(256))
    type = Column(ChoiceType(WORKOUT_TYPE),
                  nullable=False)
    sex = Column(ChoiceType({MAN: MAN, WOMAN: WOMAN}))

    _idx = Index('workout_id_index', 'id')


class Nutrition(BaseModel):
    __tablename__ = 'nutritions'

    id = Column(Integer, Sequence('nutrition_id_seq'), primary_key=True)
    name = Column(String(32))
    type = Column(ChoiceType(NUTRITION_TYPE), nullable=False)
    description = Column(String(256))
    sex = Column(ChoiceType({MAN: MAN, WOMAN: WOMAN}))

    _idx = Index('nutrition_id_index', 'id')


class NutritionMeal(BaseModel):
    __tablename__ = 'nutrition_meals'

    id = Column(Integer, Sequence('nutrition_meal_id_seq'), primary_key=True)
    time = Column(Time)
    mealtime = Column(String(32))
    nutrition_id = Column(Integer, ForeignKey('nutritions.id'))

    _idx = Index('nutrition_meal_id_index', 'id')


class Meal(BaseModel):
    __tablename__ = 'meals'

    id = Column(Integer, Sequence('meal_id_seq'), primary_key=True)
    name = Column(String(256))
    amount = Column(String(32))
    nutrition_meal_id = Column(Integer, ForeignKey('nutrition_meals.id'))

    _idx = Index('meal_id_index', 'id')


class UserToNotifyAboutNutritionMeal(BaseModel):
    __tablename__ = 'user_to_notify_about_nutrition_mealtimes'

    id = Column(Integer, Sequence('user_to_notify_about_nutrition_mealtime_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    nutrition_id = Column(Integer, ForeignKey('nutritions.id'))

    _idx = Index('user_to_notify_about_nutrition_mealtime_id_index', 'id')


async def create_database():
    await database.set_bind(DATABASE_URL)
    try:
        await database.gino.create_all()
    except InvalidRequestError:
        pass
