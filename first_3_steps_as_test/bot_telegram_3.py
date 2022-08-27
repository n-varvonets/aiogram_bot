from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os, json, string

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот вышел в онлайн')

'''******************************КЛИЕНТСКАЯ ЧАСТЬ*******************************************'''


@dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    try:
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
    # 1) т.к. любая смс в чат(не команда) попадает сюда, то устрогим проверку

    if {i.lower().translate(str.maketrans('','', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenzured.json')))) != set():  # т.е. если наше множество слов из полученного смс - не пустое,
        # то єто значит что сообщение с матом

    # из собьітия message берем наш текст и делим по пробелам...
    # потом переводим полученное слово в нижний регистр + нужно убрать маскирующие знаки($$ма!т).. для єтого у списков
    # есть метод translate()  в которьій необходимо передать "макет изменений символов в строке". там 3 агрумента:
    # 1ьій - єто что менять(в нашем случае пустую строку)
    # 2ой - на что менять
    # 3м аргументом указівается какие аргументьі из строки нужно убрать, т.е. все знаки пунктуации(что бьі вручную не перечислять -
    # возьмем его из модуля стринг)... +
    # по сути нам необходимо сравнить два огромньіх списка: intersection() - позволит нам очень бістро сравнить на то,
    # есть ли совпадения или нет....
    # в качестве агрумента задаем множество(set()) новое мнжество слов(наша цензура), читая данньіе из нашего json

        await message.reply('Матьі запрещеньі')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
