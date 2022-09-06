from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
"""т.к. МАШИННОЕ СОСТОЯНИЕ  ползволяет полшьзователю задать ряд взаимосвязанньх вопросов
 и запомнить егото нужно использовать бд для єтого"""
from aiogram.contrib.fsm_storage.memory import MemoryStorage # данньій класс позволит хранить ответьі
# пользователей в оперативной памят(т.е. только для разработки)
# + aiogram поддерживает Mongo и Redis

storage = MemoryStorage()


# правильно импортировать переменную окружения. надо разобраться
# bot = Bot(token=os.getenv('TOKEN'))

bot = Bot(token='5688669235:AAFtBqD97yzmr_aP4r2QUPOHVbWagiCQ2DU')  # так неправильно делать, но для разработки - можно
dp = Dispatcher(bot, storage=storage)

