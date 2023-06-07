import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

# load environment
load_dotenv()

# bot - server that interacts with API Telegram
bot = Bot(os.getenv("TOKEN", "Your API token"))
dp = Dispatcher(bot)