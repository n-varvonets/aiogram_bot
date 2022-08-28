import json, string
from create_bot import bot
from aiogram import types, Dispatcher


# @dp.message_handler()
async def censor_words(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('cenzured.json')))) != set():
        await message.reply('Матьі запрещеньі')
    else:
        try:
            await bot.send_message(message.from_user.id, message.text)
        except:
            await message.reply('Общение с ботом через лс. Напишите ему:\nhttps://t.me/aiogram_first_try_bot')


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(censor_words)
