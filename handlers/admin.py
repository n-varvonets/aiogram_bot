from aiogram.dispatcher import FSMContext  # в наших хендлерах будем указьівать что он используется в машинном состоянии
from aiogram.dispatcher.filters.state import State, StatesGroup  #
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot

ID = None  # для модератора при вьзове командьі 'moderator'


# создадим класс наших состояний
class FSMAdmin(StatesGroup):
    """
    В данном классе будет 4 состояния... т.е. 4 пункта последовательньіх вопросов
    """
    photo = State()
    name = State()
    description = State()
    price = State()


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
    await bot.send_message(message.from_user.id, "Привет, мой Бог!")  # , reply_markup=)
    await message.delete()


# @dp.message_handler(commands='Загрузить команда', state=None)
async def fsm_cmd_start(message: types.Message):
    """начало диалога загрузки нового пункта меню + проверка на модератора(админа группьі)"""
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()  # ВАЖНО а) здесь мьі указіваем какой хендлер дергать FSMAdmin.photo
        await message.reply('Загрузите фото')


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
        await message.reply('Введите price')


# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    """
    таким же образом с ценой FSMAdmin + записьіваем наш словарь в
    машинной памяти (бд или сейчас как пример в паямть системьі)
    """
    async with state.proxy() as data:
        data['price'] = float(message.text)

    # до вьізва ниже метода финиш() нужно передать/записать данньіе, а то пропадут..
    async with state.proxy() as data:
        await message.reply(str(data))

    # sql_add(state)

    await state.finish()


def register_handlres_admin(dp: Dispatcher):
    # 1)проверка на админа:
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    # 2.1)наша сама форма/спсиок/память_маш_состояния, которую последовательно заполняем:
    dp.register_message_handler(fsm_cmd_start, commands=['Загрузить'], state=None)
    # 2.2)для отменьі ввода формь(порядок - ВАЖЕН. для работьі во всей формьі - СРАЗУ после назначения состяния..set()):
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    # ignore_case=True - неважно какой регистр. + можно фильровать текст на (КЛЮЧЕВОЕ СЛОВО в тексте) через lamda (https://i.imgur.com/y5lwtTP.png)
    # 2.3) продолжаем работу состояния памяти формьі
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)

