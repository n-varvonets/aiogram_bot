import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")
# API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
API_TOKEN = '5491143378:AAGSoKRL7S4NeQAhcumfGPDOJlzUJUOf7nQ'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# dp.middleware.setup(AccessMiddleware(ACCESS_ID))



