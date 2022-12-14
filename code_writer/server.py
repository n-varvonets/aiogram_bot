import logging
import os, time, datetime
import keyboards.main_navigation as nav
from aiogram.types.message import ContentType
from app.create_bot import dp, bot
from aiogram import executor, types
from db import db
from pycoingecko import CoinGeckoAPI

logging.basicConfig(level=logging.INFO)

PATH_TO_DB_FILE = os.path.join("", "db/code_writer.db")
my_orm = db.Database(PATH_TO_DB_FILE)
LiqPay_TOKEN = '632593626:TEST:sandbox_i15590008377'
cg = CoinGeckoAPI()
ADMIN_ID = 402431758


def days_to_seconds(days):
    return days * 24 * 60 * 60


def time_sub_last_days(get_time_db):
    """
    Count time for end of the subscription
    :param get_time_db: secs from time() + 30 days taken from db
    :return:
        - if last_time > 0 will return last time in secof user subcription
        - else, user's sub is end
    """
    time_now = int(time.time())
    last_time = int(get_time_db) - time_now

    if last_time <= 0:
        return False
    else:
        # поситваем секы в дни или месяцы с помощью datetime(переводит наши секи в дни, часы или же месяцы)
        dt = str(datetime.timedelta(seconds=last_time))
        return dt


@dp.message_handler(commands=['start'])
async def start_and_register(message: types.Message):
    """
    if our user is not yet registered (not found in his database), then register him...
    else it was found in the database - we send him SMS warning that he is already registered
    """
    if not my_orm.user_exist(message.from_user.id):  # это айдишник пользователя в телеге
        my_orm.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Set your nickname")
    else:
        await bot.send_message(message.from_user.id, "You is already registered", reply_markup=nav.main_menu)


@dp.message_handler(commands=['send_mail'])
async def send_mailing(message: types.Message):
    """
    Mails can send only admin(add checking on admin account).
    # если после регистрации пользователь нажал заблокировать бота, то мы не сможем ему отправить смс..
    # поэтому try.. и в если пометить его неактивным, а если смс отправиться, хотя он был неактивным,
    # тогда сделаем его активным
    после чего уведомляем админа об успешной рассылке
    * message_handler следует поместить выше хендлера отлавливания простого текста
    """
    if message.chat.type == 'private':
        if message.from_user.id == ADMIN_ID:
            text = message.text[
                   :11]  # получаем текст сообщания от админа и срезаем первые 11 букв ['send_mail'] 9 + пробел(\n)
            users = my_orm.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)  # row[0] - айдишник пользователя
                    if int(row['active']) != 1:
                        my_orm.set_active(row[0], 1)
                except:
                    my_orm.set_active(row[0], 0)

            await bot.send_message(message.from_user.id, "Sending mails - done")


@dp.message_handler()
async def bot_msg(message: types.Message):
    """
    iogram can check type of chat and work only with private chat
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

            user_sub = time_sub_last_days(my_orm.get_time_subscription(message.from_user.id))
            if user_sub == False:
                user_sub = "\nYou don't have any subscription yet"
            else:
                user_sub = "\nSubscription: " + user_sub
            await bot.send_message(message.from_user.id, "Your nickname is " + nickname + user_sub)

        elif message.text == '❤️SUBSCRIPTION':
            await bot.send_message(message.from_user.id, "You can get something with the month subscription",
                                   reply_markup=nav.sub_inline_markup)

        # elif message.text == '✅️SUBSCRIDED FUNC':
        #     if my_orm.get_time_subscription_bool(message.from_user.id):
        #         """т.е. если у юзера есть подписка - мы что-то делаем"""
        #         await bot.send_message(message.from_user.id, "You got the access!")
        #     else:
        #         await bot.send_message(message.from_user.id, "Buy month subscription")

        elif message.text == '💰 COINS':
            if my_orm.get_time_subscription_bool(message.from_user.id):
                """т.е. если у юзера есть подписка - мы что-то делаем"""
                await bot.send_message(message.from_user.id, "You got the access to coins",
                                       reply_markup=nav.crypto_list)
            else:
                await bot.send_message(message.from_user.id, "Buy the month subscription for getting access to coins 💰")


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
                    await bot.send_message(message.from_user.id, f"Hi, {message.text} 😀",
                                           reply_markup=nav.main_menu)
            else:  # а если пользх  ователь уже прошел "этап регистрации" и написал что-то непонятное в диалог
                await bot.send_message(message.from_user.id, "wtf?")


@dp.callback_query_handler(text_contains='cc_')
async def crupto_currency(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    callback_data = callback.data
    currency = str(callback_data[3:])
    result = cg.get_price(ids=currency, vs_currencies='usd')
    await bot.send_message(callback.from_user.id,
                           f'Cryptocoin: {currency}\n'
                           f'Cost at the time: {result[currency]["usd"]}$',
                           reply_markup=nav.crypto_list)


@dp.callback_query_handler(text='submonth')
async def submonth(callback: types.CallbackQuery):
    """callback form user for delete his msg and show to user our product"""
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Subscription",
        description="My description of product",
        payload="month_sub",
        provider_token=LiqPay_TOKEN,
        currency="UAH",
        start_parameter="test_bot",
        prices=[
            {
                "label": "грн",
                "amount": 5000
            }
        ]
    )
    # payload - условное название нашего товара, которое будем подхватиывать дальше
    # start_parameter - если пустой, то генерирует общий платежный счет ДЛЯ ВСЕХ пользователей, а если
    # в нем что-то указано, то генериуется отдельный счет для КАЖДОГО пользователя
    # "amount" - грн 50, а указываем 5000 - потому что считаются еще копейки(без запятой)


@dp.pre_checkout_query_handler()
async def process_pre_check_out_query(pre_check_out_query: types.PreCheckoutQuery):
    """Submit existing of our product"""
    await bot.answer_pre_checkout_query(pre_check_out_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    """
    decorator process all payments using payload
    """
    if message.successful_payment.invoice_payload == "month_sub":
        time_sub = int(time.time()) + days_to_seconds(
            30)  # time() секунды прошедшие с 1980 по наше время + прибавляем 30 дней в сек - с помощью этого считаем ьконец подписки
        my_orm.set_time_subscription(message.from_user.id, time_sub)
        await bot.send_message(message.from_user.id, "You was successfully subscribed per month")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
