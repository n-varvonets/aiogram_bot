import logging
from finance_bot.app.create_bot import dp
from aiogram import executor
from db import db

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    db.check_db_exists()
    print('Бот вышел в онлайн')


from handlers import client, budjet

budjet.register_handlres_budjet(dp)
client.register_handlres_clients(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
