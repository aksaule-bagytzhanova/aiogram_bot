import os
from aiogram.dispatcher.filters.state import State, StatesGroup

TOKEN = os.environ.get("TOKEN")
WEATHER_TOKEN = os.environ.get("WEATHER_TOKEN")
url_img = r'E:\Aim\projects for protfolio\work projects\aiogram_bot\img'


class Form(StatesGroup):
    city = State()
    tg = State()
