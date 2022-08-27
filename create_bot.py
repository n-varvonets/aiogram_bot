from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os

# правильно импортировать переменную окружения. надо разобраться
# bot = Bot(token=os.getenv('TOKEN'))

bot = Bot(token='5688669235:AAFtBqD97yzmr_aP4r2QUPOHVbWagiCQ2DU')  # так неправильно делать, но для разработки - можно
dp = Dispatcher(bot)
