import logging
import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
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
        # User is not in any state, ignoring
        return

    # Cancel state and inform user about it
    await state.finish()
    await message.reply('Cancelled.')


@dp.message_handler(state=config.Form.city)
async def process_name(message: types.Message, state: FSMContext):
    """Process user name"""

    # Finish our conversation
    async with state.proxy() as data:
        data['city'] = message.text

    await message.reply(f"{message.text}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)