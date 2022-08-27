from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher  # улавливает собьітия в чате и соответсвующим потом образом прописьівае логику
from aiogram.utils import executor  # позволит нам вьійти в онлайн

import os  # что бьі взять токен из переменной средьі окружения

bot = Bot(token=os.getenv('TOKEN'))  # создаем инстанс бота передвая в него токен нашего бота
dp = Dispatcher(bot)  # улавлием собьітия, которіе происходят с нашим ботом

# бота можно запустить в 2х реимах:
# - longpooling: в єтом режиме локально бот постоянно опрашивает сервер на наличия измений
# - webhook: наш бот деплоится н сервере(у него появляется апишка, url)  и теперь не бот опрашивает сервер телеграмма,
# а сервер телеграмма посьілает измениния на нашу апи, когда появляются изменения

@dp.message_handler() # сюда будут попадать любьіе текстовіье сообзщаения, которьіе отправляют нашему боту в чат
async def echo_send(message: types.Message):

    # к примеру отправить ответное смс нашим ботом 3мя вариками:
    await message.answer(message.text)
    # await message.reply(message.text)  # упоминает автора сообщения и отвечает ему тем же сообщением
    # await bot.send_message(message.from_user.id, message.text)  # данньій ответ будет отправлять смс НАПРЯМУЮ В ЛИЧКУ. он сработает ТОЛЬКО в том случае,
    # пользователь когда уже писал ПЕРВЬІМ нашему боту(ну или пользователь добавился к нашему боту в контактьі)




executor.start_polling(dp, skip_updates=True)  # skip_updates = false -  будет означать что когда бот не онлайн, то ему будут приходить сообщения...
# и когда бот вьідет в онлайн, то его засьіпет всемя єтими собщениями.. (обьічно не нужно)

