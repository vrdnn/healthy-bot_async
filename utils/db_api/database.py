from datetime import date, timedelta

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.exceptions import BotBlocked
from gino import Gino
from sqlalchemy import String, Index, Sequence, sql, DateTime, func, and_
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from data.config import DATABASE_URL
from .types import ChoiceType
from .constants import WEIGHT_LOSS, WEIGHT_GAIN, WEIGHT_TONE

Base = declarative_base()

database = Gino()


class BaseModel(database.Model):
    query: sql.Select

    @classmethod
    async def filter(cls, id: int):
        return await cls.query.where(cls.id == id).gino.all()

    @classmethod
    async def all(cls):
        return await cls.query.gino.all()

    @classmethod
    async def get(cls, id: int):
        return await cls.query.where(cls.id == id).gino.first()

    @classmethod
    async def get_or_create(cls, **kwargs):
        obj = None
        if 'id' in kwargs:
            obj = await cls.get(kwargs.get('id'))
        if not obj:
            obj = await cls.create(**kwargs)
        return obj

    @classmethod
    async def count(cls) -> int:
        return await database.func.count(cls.id).gino.scalar()


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    first_name = Column(String(128))
    username = Column(String(128))

    _idx = Index('user_id_index', 'id')

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
    gramms = Column(Integer)
    product = Column(String(128))

    _idx = Index('user_calories_per_days_id_index', 'id')

    @classmethod
    async def for_day(cls, date_obj: date):
        return cls.query.where(and_(cls.created_at >= date_obj, cls.created_at < date_obj + timedelta(1))).gino.all()


class Exercise(BaseModel):
    __tablename__ = 'exercises'

    id = Column(Integer, Sequence('exercise_id_seq'), primary_key=True)
    name = Column(String(32))
    description = Column(String(32))

    _idx = Index('exercise_id_index', 'id')


class WorkoutIteration(BaseModel):
    __tablename__ = 'workout_iterations'

    id = Column(Integer, Sequence('workout_iteration_id_seq'), primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    amount = Column(Integer)


workout_iteration_association_table = Table(
    'workout_iterations', Base.metadata,
    Column('workout_iteration_id', ForeignKey('workout_iterations.id')),
    Column('workout_id', ForeignKey('WORKOUTS.id'))
)


class Workout(BaseModel):
    __tablename__ = 'WORKOUTS'

    id = Column(Integer, Sequence('workout_id_seq'), primary_key=True)
    name = Column(String(32))
    description = Column(String(32))
    type = Column(ChoiceType({WEIGHT_LOSS: WEIGHT_LOSS, WEIGHT_GAIN: WEIGHT_GAIN, WEIGHT_TONE: WEIGHT_TONE}),
                  nullable=False)
    iterations = relationship("WorkoutIteration", secondary=workout_iteration_association_table)

    _idx = Index('workout_id_index', 'id')


async def create_database():
    await database.set_bind(DATABASE_URL)
    try:
        await database.gino.create_all()
    except InvalidRequestError:
        pass
