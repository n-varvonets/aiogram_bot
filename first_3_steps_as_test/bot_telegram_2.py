from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


async def on_startup(_):
    """ єто при SetUp функция, которую пробрасьіваем в executor nhtnmbv gfhfvtnhjv"""
    # когда запускаем бот при помщи pooling - очень полезно вьівести в консоль смс о работьі
    print('Бот вышел в онлайн')

    # + дальше можно будеть здесь подключать бд

'''******************************КЛИЕНТСКАЯ ЧАСТЬ*******************************************'''


@dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    # отправим сообщения от бота КОНКРЕТНО в личку пользователя с группьі
    try:  # в случае если пользователь не добавлся к боту - обработаем ошибку
        await bot.send_message(message.from_user.id, 'Glad to join us')
    except:
        await message.reply('Общение с ботом через лс. Напишите ему:\nhttps://t.me/aiogram_first_try_bot')


@dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')


@dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'ул. Колбасная 15')


# @dp.message_handler(commands=['Меню'])
# async def pizza_menu_command(message : types.Message):
# 	for ret in cur.execute('SELECT * FROM menu').fetchall():
# 	   await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')

'''*******************************АДМИНСКАЯ ЧАСТЬ*******************************************'''

'''*********************************ОБЩАЯ ЧАСТЬ*********************************************'''


@dp.message_handler()
async def echo_send(message: types.Message):
    # к примеру отправить ответное смс нашим ботом 3мя вариками:
    await message.answer(message.text)
    # await message.reply(message.text)  # упоминает автора сообщения и отвечает ему тем же сообщением
    # await bot.send_message(message.from_user.id, message.text)  # данньій ответ будет отправлять смс НАПРЯМУЮ В ЛИЧКУ. он сработает ТОЛЬКО в том случае,
    # пользователь когда уже писал ПЕРВЬІМ нашему боту(ну или пользователь добавился к нашему боту в контактьі)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  # skip_updates = false -  будет означать что когда бот не онлайн, то ему будут приходить сообщения...
# и когда бот вьідет в онлайн, то его засьіпет всемя єтими собщениями.. (обьічно не нужно)
