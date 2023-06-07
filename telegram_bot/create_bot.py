import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# load environment
load_dotenv()

storage = MemoryStorage()

# bot - server that interacts with API Telegram
bot = Bot(os.getenv("TOKEN", "Your API token"))
dp = Dispatcher(bot, storage=storage)