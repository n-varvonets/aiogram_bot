from aiogram import types
from exceptions import exceptions
from app import expenses, msg_answers
from app.categories import Categories
from aiogram.dispatcher import Dispatcher
from keyboards import kb_client  # варик с кнопками
from inlines import client_btns


async def send_welcome(message: types.Message):
    """Sends a welcome message"""

    await message.answer(
        f"Бажаю здоров'я, {message.from_user.first_name}! 🙂 \n\n"

        "Для того щоб почати вести облік своїх фінансів - в основному\n"
        "чаті введіть суму та назву послуги вашої витрати,\n\n ➡️ наприклад: 100 кава")

    await message.answer(msg_answers.start_back_menu_2,
                         # reply_markup=kb_client
                         reply_markup=client_btns.welcome_btns
                         )


async def help_cmd(message: types.Message):
    """Отображает пример правильного сообщения к боту
     и дает команду просмотра доступньіх категории категории"""

    await message.answer(msg_answers.help_answer_1)
    await message.answer(msg_answers.help_answer_2, reply_markup=client_btns.back_to_main_btn)


async def del_expense(message: types.Message):
    """Deletes one expense record by its ID"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Видалив"
    await message.answer(answer_message, reply_markup=client_btns.back_to_main_btn)


async def categories_list(message: types.Message):
    """Sends a list of expense categories"""
    categories = Categories().get_all_categories()
    answer_message = "Категорії витрат:\n\n " + \
                     (f"\n ".join(
                         [f"{idx_cat + 1}.) " + category.name.capitalize() + ': ' + ", ".join(category.aliases) + ';'
                          for
                          idx_cat, category in enumerate(categories)])
                      + "\n\n⚠️ тільки перші 4 категрії відносяться до базових витрат")
    await message.answer(answer_message, reply_markup=client_btns.back_to_main_btn)


async def today_statistics(message: types.Message):
    """Sends today's spending statistics"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message, reply_markup=client_btns.back_to_main_btn)


async def month_statistics(message: types.Message):
    """Sends spending statistics of the current month"""
    try:
        answer_message = expenses.get_month_statistics()
        await message.answer(answer_message, reply_markup=client_btns.back_to_main_btn)
    except:
        await message.answer("")


async def list_expenses(message: types.Message):
    """Sends the last few expense records"""
    last_expenses = expenses._get_last_five_expenses()
    if not last_expenses:
        await message.answer("Ще не зроблено жодної витрати")
        await message.answer(msg_answers.start_back_menu_1)
        return

    last_expenses_rows = [
                             f"{expense[0].id} витрата: '{' '.join(expense[1].split()[1:])}' у размірі {expense[0].amount} грн занесена до категоріїї \n" \
                             f"'{expense[0].category_name}' - натисни /del{expense[0].id} щоб видалити  запис"

                             for expense in last_expenses][::-1]

    answer_message = "Останні збережені витрати:\n\n " + "\n\n ".join(last_expenses_rows)

    await message.answer(answer_message, reply_markup=client_btns.back_to_main_btn)


async def add_expense(message: types.Message):
    """Adds a new expense"""
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"{expense.amount} грн було додано до '{expense.category_name}' категорії.\n\n"
    )
    await message.answer(answer_message, reply_markup=client_btns.back_to_main_btn)


def register_handlres_clients(dp: Dispatcher):
    """register our funcs to handlers of client logic user story"""
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(help_cmd, commands=['help'])
    dp.register_message_handler(del_expense, lambda message: message.text.startswith('/del'))
    dp.register_message_handler(categories_list, commands=['categories'])
    dp.register_message_handler(today_statistics, commands=['today'])
    dp.register_message_handler(month_statistics, commands=['month'])
    dp.register_message_handler(list_expenses, commands=['expenses'])
    dp.register_message_handler(add_expense)
