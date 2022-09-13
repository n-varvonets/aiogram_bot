from aiogram import types
from inlines import budjet_btns, client_btns
from app.create_bot import dp
from app import expenses, msg_answers
from app.categories import Categories
from aiogram.dispatcher import Dispatcher


async def back_to_main_menu_cb(callback: types.CallbackQuery):
    """Sends a welcome message"""

    await callback.message.answer(msg_answers.start_back_menu_1)
    await callback.message.answer(msg_answers.start_back_menu_2,
                                  # reply_markup=kb_client
                                  reply_markup=client_btns.welcome_btns)
    await callback.answer()


async def help_cb(callback: types.CallbackQuery):
    """Отображает пример правильного сообщения к боту
     и дает команду просмотра доступньіх категории категории"""
    await callback.message.answer(msg_answers.help_answer_1)
    await callback.message.answer(msg_answers.help_answer_2, reply_markup=client_btns.back_to_main_btn)
    await callback.answer()


async def today_statistics_cb(callback: types.CallbackQuery):
    answer_message = expenses.get_today_statistics()
    await callback.message.answer(answer_message, reply_markup=client_btns.back_to_main_btn)
    await callback.answer()


async def list_expenses_cb(callback: types.CallbackQuery):
    """Sends the last few expense records"""
    last_expenses = expenses._get_last_five_expenses()
    if not last_expenses:
        await callback.message.answer("Ще не зроблено жодної витрати")
        await callback.message.answer(msg_answers.start_back_menu_1)
        await callback.answer()
        return

    last_expenses_rows = [
                             f"#{expense[0].id} '{' '.join(expense[1].split()[1:])}' у размірі {expense[0].amount} грн занесена до категоріїї \n" \
                             f"'{expense[0].category_name}' - натисни /del{expense[0].id} щоб видалити  запис"

                             for expense in last_expenses][::-1]

    answer_message = "Останні збережені витрати:\n\n " + "\n\n ".join(last_expenses_rows)

    await callback.message.answer(answer_message, reply_markup=client_btns.back_to_main_btn)
    await callback.answer()


async def month_statistics_cb(callback: types.CallbackQuery):
    """Sends spending statistics of the current month"""
    try:
        answer_message = expenses.get_month_statistics()
        await callback.message.answer(answer_message, reply_markup=client_btns.back_to_main_and_set_budjet_btn)
        await callback.answer()
    except:
        await callback.message.answer("")


async def categories_list_cb(callback: types.CallbackQuery):
    """Sends a list of expense categories"""
    categories = Categories().get_all_categories()
    answer_message = "Категорії витрат:\n\n " + \
                     (f"\n ".join(
                         [f"{idx_cat + 1}.) " + category.name.capitalize() + ': ' + ", ".join(category.aliases) + ';'
                          for
                          idx_cat, category in enumerate(categories)])
                      + "\n\n⚠️ тільки перші 4 категрії відносяться до базових витрат")
    await callback.message.answer(answer_message, reply_markup=client_btns.back_to_main_btn)
    await callback.answer()


def register_clients_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(back_to_main_menu_cb, text='main_menu')
    dp.register_callback_query_handler(help_cb, text='help_cb_btn')
    dp.register_callback_query_handler(today_statistics_cb, text='today_cb_btn')
    dp.register_callback_query_handler(list_expenses_cb, text='expenses_cb_btn')
    dp.register_callback_query_handler(month_statistics_cb, text='month_cb_btn')
    dp.register_callback_query_handler(categories_list_cb, text='categories_cb_btn')
