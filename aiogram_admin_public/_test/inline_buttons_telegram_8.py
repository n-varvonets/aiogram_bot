from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

users_already_voted = {}

bot = Bot(token='5688669235:AAFtBqD97yzmr_aP4r2QUPOHVbWagiCQ2DU')  # так неправильно делать, но для разработки - можно
dp = Dispatcher(bot)

# 1)Кнопка-ссьілка
url_kb = InlineKeyboardMarkup(
    row_width=2)  # инициализируем класс кнопок-ссьілок, указьвая их кол-во в одном ряду(т.е. по две кнопки в ряд)
url_btn1 = InlineKeyboardButton(text='btn_for_youtube', url='https://www.youtube.com/')
url_btn2 = InlineKeyboardButton(text='btn_for_google', url='https://www.google.com.ua/')
url_kb.add(url_btn1, url_btn2)


@dp.message_handler(commands='websites')
async def url_btn_commands(message: types.Message):
    await message.answer('Your websites:', reply_markup=url_kb)


# 2) Callback кнопки. К примеру реализуем систему лайков и дизлайков.
# callback_data - имя собьітия, которое после нажатия произойдет. Туда можно передать
# произвольньіе данньіе или наш определенньій хендлер обработчик
callback_btns_kb = InlineKeyboardMarkup(row_width=1)
callback_btn1_like = InlineKeyboardButton(text="Like", callback_data='like_1')
callback_btn2_dislike = InlineKeyboardButton(text="Dislike", callback_data='like_-1')
callback_btns_kb.add(callback_btn1_like).add(callback_btn2_dislike)


@dp.message_handler(commands='test_callback_btn_votes')
async def test_callback_btn(message: types.Message):
    await message.answer(
        'Do your like or dislike the post:\nhttps://www.google.com/search?q=nature&sxsrf=ALiCzsb22b0XXQrHN1toMIlywLy9TP_Dcw:1661760383048&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiG8NTqy-v5AhWE6CoKHd1pBHsQ_AUoAXoECAEQAw&biw=1920&bih=975&dpr=1#imgrc=hE13wqAXPgtskM',
        reply_markup=callback_btns_kb)


# @dp.callback_query_handlers(text='www')
@dp.callback_query_handler(Text(startswith='like_'))  # можно используя фильтр. таким образом хендлер сможет обработать два колбека удовлетворяющие условия фильтра
async def like_dislike_call(callback: types.CallbackQuery):  # CallbackQuery - обьязательно нужно указать для колбека

    res = int(callback.data.split('_')[1])  # для дизлайков в ответе у нас будет 1 или -1
    if f'{callback.from_user.id}' not in users_already_voted:  # делаем проверку, что бьі пользователь не мог голосовать много раз подряд
        users_already_voted[f'{callback.from_user.id}'] = res
        await callback.answer('Вьі проголосвали')
    else:
        await callback.answer('Вьі уже проголосвали', show_alert=True)  # show_alert=True - смс в виде попапа

    # await callback.answer('нажата инлайн кнопка')   # отобразится после нажатия командьі в виде попапа в чате
    # await callback.message.answer('нажата инлайн кнопка')  # напишет ответ в чат
    # await callback.answer()  # await без аргумента закроет часики на кнопке callback


# 3) стартуем наш бот
executor.start_polling(dp, skip_updates=True)
