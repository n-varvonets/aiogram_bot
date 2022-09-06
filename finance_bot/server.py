import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import markdown
from aiogram.dispatcher.filters.state import State, StatesGroup

import db
import exceptions
import expenses
from categories import Categories
from middlewares import AccessMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

API_TOKEN = "5429933851:AAHhEy1kyBhZDCLIAdXMAPW3lS7gTZopKSo"
# API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

ACCESS_ID = 40243175
# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")

# PROXY_URL = os.getenv("TELEGRAM_PROXY_URL")
# PROXY_AUTH = aiohttp.BasicAuth(
#     login=os.getenv("TELEGRAM_PROXY_LOGIN"),
#     password=os.getenv("TELEGRAM_PROXY_PASSWORD")
# )

storage = MemoryStorage()  # для FSM state

# bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
dp = Dispatcher(bot, storage=storage)


# dp.middleware.setup(AccessMiddleware(ACCESS_ID))


# создадим класс наших состояний
class FSMBudjet(StatesGroup):
    """
    В данном классе будет 4 состояния... т.е. 4 пункта последовательньіх вопросов
    """
    total_income = State()
    month_planing_base_expenses = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    # await message.answer(
    #     "Моя ціль - допомоти Вам вести облік своїх фінансів 🤓 Збережу всі Ваші витрати, які автоматично поділю по категоріям і проведу відповідну базову аналітику 🧐.")

    await message.answer(
        f"Бажаю здоров'я, {message.from_user.first_name}! 🙂 \n\n"

        "Для того щоб почати вести облік своїх фінансів - в основному\n"
        "чаті введіть суму та назву послуги вашої витрати,\n\n ➡️ наприклад: 100 кава")

    await message.answer(
        "У вас є можливість скористатись такими швидкими командами:\n\n"
        
        "/expenses - останні мої витрати\n"
        "/set_budget - задати місячний бюджет\n"
        "/today - статистика витрат за сьогодні\n"
        "/month - статистика витрат за поточний місяць\n"
        "/categories - доступні категоріі витрат\n"
        "/help - додатков інформація про мене та мої можливості"

    )


@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    """Отображает пример правильного сообщения к боту
     и дает команду просмотра доступньіх категории категории"""

    await message.answer(
        "Витрати можно розділити по категоріям /categories\n\n"
        "Категорії витрат в свою чергу бувають 2️⃣х типів:\n\n"
        "    🔹 Базові: ті витрати, які ми щоденно робимо та щомісяно виплачуємо(таксі, продукти, квартира, поповнення інтернету, спортзал..)\n\n"
        "    🔹 Не базові: не небходні  витрати в нашому житті та які маємо."
        " контролювати у рамка обумовленного бюджету (підпіска, кава, піцца, дав у борг, донат, book, кіно і т.д.)"
    )
    await message.answer(
        "Щоб я зміг провести аналіз ваших сьогоднішніх й місячних витрат 📈 потрібно вказати Ваш бюджет:\n\n"
        "/set_budget - задати власний бюджет\n\n"
        "Бюджет має дві ключеві харатеристики:\n"
        "    - загальній Ваш місячний дохід в грн;\n"
        "    - місячні базові витрати: та сумма, яку ми приблизно разраховуємо витратити цього місяця на базові витрати.\n\n"
        "⚠️ місячні базові витрати - це частина від загального місячного дохіду та не може його перевищувати."
    )


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Видалив"
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Отправляет список категорий расходов"""
    categories = Categories().get_all_categories()
    answer_message = "Категорії витрат:\n\n " + \
                     (f"\n ".join(
                         [f"{idx_cat + 1}.) " + category.name.capitalize() + ': ' + ", ".join(category.aliases) + ';'
                          for
                          idx_cat, category in enumerate(categories)]))
    await message.answer(answer_message)


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['set_budget'], state=None)
async def set_state_total_income(message: types.Message):
    await FSMBudjet.total_income.set()
    await message.answer('Вкажіть Ваш загальний дохід за місяць, грн,\n\n'
                         '➡️  наприклад: 10000')


# @dp.message_handler(state="*", commands='відміна')
# @dp.message_handler(Text(equals='відміна', ignore_case=True), state="*")
# async def cancel_handler_state(message: types.Message, state: FSMContext):
#     """
#     Відміна заповнення форми бюджету
#     """
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await message.reply('OK')


@dp.message_handler(state=FSMBudjet.total_income)
async def set_state_month_planing_base_expenses(message: types.Message, state: FSMContext):
    """ловим первьій ответ от пользователя(photo) и пишем в словарь(память) машинного состояния по классу FSMAdmin"""
    async with state.proxy() as data:
        try:
            val_total_income = int(message.text)
            data['total_income'] = val_total_income
            await FSMBudjet.next()
            await message.answer('Тепер вкажіть місячну сумму ваших базових витрат, грн.\n\n'
                                 '/help - детальніше про базові витрати')

        except:
            await message.answer('Відповідь повинна бути у числовому форматі')


@dp.message_handler(state=FSMBudjet.month_planing_base_expenses)
async def set_state_month_planing_base_expenses(message: types.Message, state: FSMContext):
    """ловим первьій ответ от пользователя(photo) и пишем в словарь(память) машинного состояния по классу FSMAdmin"""
    check_type_and_comparison = False

    async with state.proxy() as data:
        try:
            # check for type of recieved msg
            val_month_planing_base_expenses = int(message.text)
            data['month_planing_base_expenses'] = val_month_planing_base_expenses

            if tuple(data.values())[0] > tuple(data.values())[1]:  # проверка на то указал ли клиент верно... а именно установил ли он месячньіх доход больше числа базовьіх растрат
                # если все хорошо, то записуем его в бд отметив флаг проверки в тру
                check_type_and_comparison = True
            else:
                # в противном уведовмляем ему об єтом и кидаем заново заполнить форму бюджета
                await message.answer(
                                     '⚠️ Загальний дохід за місяць повинен бути більшим,\n'
                                     ' ніж запланована місячна сумму базових витрат\n\n'
                                     '/set_budget - перезаповнити форму')
                await state.finish()

        except:
            await message.answer('Відповідь повинна бути у числовому форматі')



    if check_type_and_comparison:

        await db.set_budget(state)
        await message.answer('Ваш місяний бюджет оновленно:\n'
                             f'    - загальний дохід за місяць: {data["total_income"]} грн\n'
                             f'    - місячна сумму базових витрат: {data["month_planing_base_expenses"]} грн')
        await state.finish()


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """Отправляет статистику трат текущего месяца"""
    try:
        answer_message = expenses.get_month_statistics()
        await message.answer(answer_message)
    except:
        await message.answer("")


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о расходах"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Ще не зроблено жодної витрати")

    last_expenses_rows = [
        f"{expense.amount} грн. на {expense.category_name} — натисни "
        f"/del{expense.id} щоб видалити витрату"
        for expense in last_expenses]
    answer_message = "Останні збережені витрати:\n\n* " + "\n\n* " \
        .join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет новый расход"""
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Додані витрати {expense.amount} грн на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
