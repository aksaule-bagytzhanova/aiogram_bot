import logging
import config
import main_weather
import main_converted
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import random
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = config.TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

memstore = MemoryStorage()
dp = Dispatcher(bot, storage=memstore)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Приветствую ВАС!\nЯ бот компании\nЯ имею команды "
                        "как\n /get_Weather \n /get_Exchange \n /get_Cute \n "
                        "/create_Poll")


@dp.message_handler(commands=['get_Weather'])
async def send_Weather(message: types.Message):
    await config.Form.city.set()
    await message.answer('Погоду какого города узнать?')


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    """Allow user to cancel action via /cancel command"""

    current_state = await state.get_state()
    if current_state is None:

        return

    await state.finish()
    await message.reply('Cancelled.')


@dp.message_handler(state=config.Form.city)
async def process_name(message: types.Message, state: FSMContext):
    # Finish our conversation
    async with state.proxy() as data:
        data['city'] = message.text

    await message.reply(f"{main_weather.get_message(message.text)}")


@dp.message_handler(commands=['get_Exchange'])
async def send_Converted_Currencies(message: types.Message):
    await config.Form.tg.set()
    await message.answer('Сколько тенге перевести на доллар?')


@dp.message_handler(state=config.Form.tg)
async def process_name(message: types.Message, state: FSMContext):
    # Finish our conversation
    async with state.proxy() as data:
        data['convert'] = message.text

    await message.reply(f"{main_converted.get_coin(message.text)}")


@dp.message_handler(commands=['get_Cute'])
async def send_image(message: types.Message):
    n = random.randint(0,5)
    photo = open(f"{config.url_img}\{n}.jpg", "rb")
    await bot.send_photo(photo=photo, caption="",
                         chat_id=message.chat.id)


@dp.message_handler(commands=['create_Poll'])
async def create_poll(message: types.Message):
    await bot.send_poll(question='How are u?',
                        is_anonymous=False, options=['good', 'bad'],
                        chat_id=message.chat.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)