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
    await bot.send_message(message.from_user.id, 'ул. Колбасная 15')


# @dp.message_handler(commands=['Меню'])
# async def pizza_menu_command(message : types.Message):
# 	for ret in cur.execute('SELECT * FROM menu').fetchall():
# 	   await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['Режим_роботи'])
    dp.register_message_handler(pizza_place_command, commands=['Місце_знаходження'])
