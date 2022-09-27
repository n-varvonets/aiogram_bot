import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import app.config as conf

storage = MemoryStorage()

# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")
# API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")


bot = Bot(token=conf.API_BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

# dp.middleware.setup(AccessMiddleware(ACCESS_ID))



