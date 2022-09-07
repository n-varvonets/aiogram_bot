from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()  # для FSM state

API_TOKEN = "5429933851:AAHhEy1kyBhZDCLIAdXMAPW3lS7gTZopKSo"
# API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

ACCESS_ID = 40243175
# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")

# bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
dp = Dispatcher(bot, storage=storage)

# dp.middleware.setup(AccessMiddleware(ACCESS_ID))

