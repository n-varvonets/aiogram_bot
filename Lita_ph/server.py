import logging
import app.config as conf, app.cenz as cenz
from app.create_bot import dp, bot
from aiogram import executor, types
from inlines.main_murkups import channel_menu

logging.basicConfig(level=logging.INFO)


def check_sub_channel(chat_member):
    """
    проверять подписку юзера на наш канал(т.е. состоив ли в нашем канале)
    :return булиан на статус left
    """
    return chat_member['status'] != 'left'


@dp.message_handler(commands=['mute'], commands_prefix="/")
async def admin_mute(message: types.Message):
    """
    the cmd will look like: /mute 60
    If user write down bed msg and this msg wasn't blocked by cenz func - admin can mute it user by cmd
        - check if admin calls current cmd
        - check if command was called not answering on some msg. only directly the command should be called!
    :param message:
    :return:
    """
    if str(message.from_user.id) == conf.ADMIN_ID:
        if not message.reply_to_message:
            await message.reply("This command should be as answer on msg")
            return

        mute_secs = int(message.text[6:])  # /mute 60 - and left only our secs
        conf.my_orm._set_mute(message.reply_to_message.from_user.id, mute_secs)
        await message.bot.delete_message(conf.CHAT_ID, mute_secs)
        await message.reply_to_message.reply(f"User was muted on {mute_secs} secs")


@dp.message_handler(content_types=['new_chat_members'])
async def user_joined(message: types.Message):
    # content_types - отлдавливает встроенные в телеге функции(например присоединение новго пользователя в чате)
    await message.answer(
        f"Welcome, {message.from_user.username}✋!\n For chatting need to subscribe on  our channel",
        reply_markup=channel_menu
    )


@dp.message_handler()
async def mess_handler(message: types.Message):
    """
    Recieve msg from user and:
        - check user in our db thought my_orm with or add new one
        - check if user is not muted
        - check subscription on our main chanel for our group for ability chatting
        - check msg on cenzored words
    :param message: 
    :return: 
    """

    if not conf.my_orm.user_exist(message.from_user.id):
        conf.my_orm.add_user(message.from_user.id)

    if not conf.my_orm._is_mute(message.from_user.id):

        if check_sub_channel(await bot.get_chat_member(chat_id=conf.CHANNEL_ID, user_id=message.from_user.id)):
            text = message.text.lower()
            for word in cenz.WORDS:
                if word in text:
                    await message.delete()
        else:
            await message.answer("For chatting need to subscribe on  our channel", reply_markup=channel_menu)
            await message.delete()
    else:
        await message.delete()
        await message.reply_to_message.reply(f"You was banned by admin")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
