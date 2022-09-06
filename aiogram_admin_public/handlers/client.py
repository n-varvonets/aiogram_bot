from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client


async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Glad to join us', reply_markup=kb_client)
    except:
        await message.reply('Общение с ботом через лс. Напишите ему:\nhttps://t.me/aiogram_first_try_bot')


async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')


async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'ул. Больничная, 15')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['Режим_роботи'])
    dp.register_message_handler(pizza_place_command, commands=['Місце_знаходження'])
