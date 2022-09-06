from aiogram.dispatcher import FSMContext  # в наших хендлерах будем указьівать что он используется в машинном состоянии
from aiogram.dispatcher.filters.state import State, StatesGroup  #
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from data_base.sql_db import sql_add_command, sql_read_all_clients, sql_fetch_all_clients, sql_delete_client
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None  # для модератора при вьзове командьі 'moderator'


# создадим класс наших состояний
class FSMAdmin(StatesGroup):
    """
    В данном классе будет 4 состояния... т.е. 4 пункта последовательньіх вопросов
    """
    photo = State()
    name = State()
    description = State()
    age = State()


# @dp.message_handler(commands['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    """
    Проверяем является ли текщий пользователь модеротором
    при условии, если пользователь ввель команду 'moderator' AND является  по факту модератором,
    в противном случае хендлер не сработает.
    Админ в телеге должен обратиться к группе, а не боту, после чего смс сразу удаляется.
    После чего, при віьзове функции, которая начинает ввод формьі(в нашем случае /Загрузить), проверяет
    совпадает ли новое global ID с тем кто ее вьізвал, если до, то она вьіполняется.
    """
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Привет, мой Бог!",
                           reply_markup=admin_kb.button_case_admin)  # reply_markup - отправляем для него клава
    await message.delete()


# @dp.message_handler(commands='Загрузить команда', state=None)
async def fsm_cmd_start(message: types.Message):
    """начало диалога загрузки нового пункта меню + проверка на модератора(админа группьі)"""
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()  # ВАЖНО а) здесь мьі указіваем какой хендлер дергать FSMAdmin.photo
        await message.reply('Загрузите свое фото')


# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    В любой машине состояния должен бьіть хендлер,которьій отменяет действия ввода формьі.
    декорируется двумя хендлерами:
        - для командьі отменьі;
        - просто написать отмена, применяя класс библиотеки dispatcher.filters
    где, "*" - означет что будет доступен при каждом візова хендлера в любом состоянии бота.
    есть спец функция библетеки get_state()
    + нужно их обе зарегистрировать в ниже функции для админа, т.к. у нас не  одно скриптовьій бот
    """
    current_state = await state.get_state()

    # исключаем возможность ошибки, если текущее состояние уже отсутвует, то ниче не делаем. в ином - закріьваем форму
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)  # ВАЖНО б) благодаря FSMAdmin.photo бот поймет
# что нужно дергать данньій хендлер
async def load_photo(message: types.Message, state: FSMContext):  # FSMContext - просто параметр аннотации(typing)
    """ловим первьій ответ от пользователя(photo) и пишем в словарь(память) машинного состояния по классу FSMAdmin"""
    async with state.proxy() as data:  # 1)открьіваем словарь(память) машинного состояния по классу FSMAdmin
        data['photo'] = message.photo[0].file_id  # и из смс дату помещаем в наш словарь класса.
        # у aiogram баблиотеки есть специальная функция отправлять бит фото по его айдишнику из отправленного смс
        await FSMAdmin.next()  # переходим к след вопросу
        # todo проверь можно ли заменить метод next(), которьій скорее всего последовательно возьмут след
        #  аттрибут класа FSMAdmin (след name по очереди задав конретньій аттрибут, которьій ХОТИМ ОЖИДАТЬ СЛЕДУЮЩИМ
        #  как в первом случае с await FSMAdmin.photo.set()
        await message.reply('Введите название')


# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    """таким же образом с именем класса FSMAdmin"""
    async with state.proxy() as data:
        data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите описание')


# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    """таким же образом с именем description  FSMAdmin"""
    async with state.proxy() as data:
        data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите age')


# @dp.message_handler(state=FSMAdmin.age)
async def load_age(message: types.Message, state: FSMContext):
    """
    таким же образом с ценой FSMAdmin + записьіваем наш словарь в
    машинной памяти (бд или сейчас как пример в паямть системьі)
    """
    async with state.proxy() as data:
        data['age'] = float(message.text)

    # до вьізва ниже метода финиш() нужно передать/записать данньіе, а то пропадут..
    await sql_add_command(state)

    await message.answer('Запись о клиенте добавлена')  # уведомляем админа об успехе создания записи

    await state.finish()


# @dp.message_handler(commands=['get_our_clients'])
async def clients_catalog(message: types.Message):
    """создадим комнду на посмотреть инфу обо всех пользователей"""
    await sql_read_all_clients(message)


# Для удаления адсмином записи в бд потребуется прописать message_handler и callback_query_handler:
# @dp.message_handler(commands=['/Удалить_клиента'])
async def delete_item(message: types.Message):
    """отобразим перед удалением всех клиентов и отправим в личку инлайн кнопку на вьізов колбека используя хендлер"""
    if message.from_user.id == ID:
        all_clients = await sql_fetch_all_clients()
        for client in all_clients:
            # 1) отправляем нашему администратору в личку сообщение о продукте
            await bot.send_photo(message.from_user.id, client[0],
                                 f'Имя: {client[1]}\nОписание: {client[2]}\nВозраст: {client[-1]}')
            # 2) отправляем инлайн кнопку в лчику, по которой если нажать активируется хенлер колбєка удаления записи
            await bot.send_message(
                message.from_user.id,
                text='^^^some warning text~~',
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text=f'Удалить клиента {client[1]}?',
                        callback_data=f'del {client[1]}'
                    )
                )
            )


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))  # callback НЕ РЕГИСТРИРУЕТСЯ в хендлерах
async def del_item_callback_run(
        callback: types.CallbackQuery):  # callback - єтот параметр можно навзать как угодно,главное указать types.CallbackQuery
    # 1)вьполним запрос на удаление записи
    await sql_delete_client(callback.data.replace('del ', ''))
    # 2) отвечаем телеграму что запрос вьіполнен и паралельно указівает какой именно запрос вьіполненнно
    await callback.answer(text=f"{callback.data.replace('del ', '')} удален(-а)", show_alert=True)


def register_handlres_admin(dp: Dispatcher):
    # 1)проверка на админа:
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    # 2.1)наша сама форма/спсиок/память_маш_состояния, которую последовательно заполняем:
    dp.register_message_handler(fsm_cmd_start, commands=['Загрузить_клиента'], state=None)
    # 2.2)для отменьі ввода формь(порядок - ВАЖЕН. для работьі во всей формьі - СРАЗУ после назначения состяния..set()):
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    # ignore_case=True - неважно какой регистр. + можно фильровать текст на (КЛЮЧЕВОЕ СЛОВО в тексте) через lamda (https://i.imgur.com/y5lwtTP.png)
    # 2.3) продолжаем работу состояния памяти формьі
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    # 2.4) Регистрируем меню
    # dp.register_message_handler(clients_catalog, commands=['get_our_clients'])
    dp.register_message_handler(clients_catalog, lambda x: 'get' and 'our' and 'clients' in x.text)
    # 2.5) Жобавим админу возможность удалить клиента(продукт)
    dp.register_message_handler(delete_item, commands=['Удалить_клиента'])




