import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# dp.middleware.setup(AccessMiddleware(ACCESS_ID))



