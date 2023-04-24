import os
from aiogram.dispatcher.filters.state import State, StatesGroup

TOKEN = os.environ.get("TOKEN")
WEATHER_TOKEN = os.environ.get("WEATHER_TOKEN")


class Form(StatesGroup):
    city = State()
