import logging
import os
import keyboards.main_navigation as nav
from app.create_bot import dp, bot
from aiogram import executor, types
from db import db

logging.basicConfig(level=logging.INFO)

PATH_TO_DB_FILE = os.path.join("", "db/code_writer.db")
my_orm = db.Database(PATH_TO_DB_FILE)


@dp.message_handler(commands=['start'])
async def start_and_register(message: types.Message):
    """
    if our user is not yet registered (not found in his database), then register him..
    else it was found in the database - we send him SMS warning that he is already registered
    """
    if not my_orm.user_exist(message.from_user.id):  # это айдишник пользователя в телеге
        my_orm.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Set your nickname")
    else:
        await bot.send_message(message.from_user.id, "You is already registered", reply_markup=nav.main_menu)


@dp.message_handler()
async def bot_msg(message: types.Message):
    """
    iogram can check type of chat
    Поскольку у нас есть динамический ввод данных(будем указывать ник)
    # пройдя проверку что его статус уже ук
    :param message: msg from user for set nickname
    :return:
    """
    if message.chat.type == 'private':
        if message.text == '👤PROFILE':
            """
            проверяем сначала заготовленный текст,
            т.е. когда пользователь нажимает на кнопку профиль, он отправляет текст '👤PROFILE'
            """
            nickname = my_orm.get_nickname(message.from_user.id)
            await bot.send_message(message.from_user.id, "Your nickname is " + nickname)

        else:
            if my_orm.get_sign_up_stage(message.from_user.id) == 'setnickname':
                # если пользователь на этапе регистрации и должен укзать ник,
                # то мы этот текст обрабатываем как ник и записываем в бд
                if len(message.text) > 15:
                    await bot.send_message(message.from_user.id, "Nickname should not be more than 15 letters")
                elif '@' in message.text or '/' in message.text:  # добавим проверку на запрещенные символы
                    await bot.send_message(message.from_user.id, "You input wrong symbols")
                else:
                    # попдая в данное условие - пользователь прошел проверки.. назнаем его новый ник
                    my_orm.set_nickname(message.from_user.id, message.text)
                    my_orm.set_sign_up_stage(message.from_user.id, "done")
                    await bot.send_message(message.from_user.id, "Регистрация прошла успешно", reply_markup=nav.main_menu)
            else:
                # а если пользхователь уже прошел "этап регистрации" и написал что-то непонятное в диалог
                await bot.send_message(message.from_user.id, "wtf?")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
