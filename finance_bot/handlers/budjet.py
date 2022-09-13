from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher import Dispatcher
from db import db
from inlines import budjet_btns, client_btns


class FSMBudjet(StatesGroup):
    """
    The class will have 2 states
    """
    total_income = State()
    month_planing_base_expenses = State()


async def set_state_total_income(message: types.Message):
    """Start filling the budget form via StateGroup"""
    await FSMBudjet.total_income.set()
    await message.answer('Вкажіть Ваш загальний дохід за місяць, грн,\n\n'
                         '➡️  наприклад: 15000 чи 15_000', reply_markup=budjet_btns.cancel_btn)


async def cancel_handler_state(message: types.Message, state: FSMContext):
    """
    Cancellation of filling out the budget form
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('ок, форма заповнення бюджету скасовано!', reply_markup=client_btns.back_to_main_btn)


async def set_state_month_total_income(message: types.Message, state: FSMContext):
    """
    Сatch the first answer total_income from the user into
    the dictionary (memory) of the machine state by class FFSMAdmin
    """
    async with state.proxy() as data:
        try:
            val_total_income = int(message.text)
            data['total_income'] = val_total_income
            await FSMBudjet.next()
            await message.answer('Тепер вкажіть місячну сумму ваших базових витрат, грн.\n\n'
                                 '➡️  наприклад: 7500 чи 7_500', reply_markup=budjet_btns.cancel_btn)

        except:
            await message.answer('Відповідь повинна бути у числовому форматі',
                                 reply_markup=client_btns.back_to_main_btn)


async def set_state_month_planing_base_expenses(message: types.Message, state: FSMContext):
    """
    Catch the second answer month_planing_base_expenses from the user by class FSMAdmin
        - check for type of recieved msg;
        - check the value if the client has set monthly income more than basic expenses...
            - if everything is good, then we write it down in the database.
            - otherwise need to inform him about this and ask him to fill out the budget form again
    """

    check_type_and_comparison = False

    async with state.proxy() as data:
        try:
            #
            val_month_planing_base_expenses = int(message.text)
            data['month_planing_base_expenses'] = val_month_planing_base_expenses

            if tuple(data.values())[0] > tuple(data.values())[1]:
                check_type_and_comparison = True
            else:
                await message.answer(
                    '⚠️ Загальний дохід за місяць повинен бути більшим,\n'
                    ' ніж запланована місячна сумму базових витрат\n\n'
                    '/set_budget - перезаповнити форму\n'
                    '/help - детальніше быльше про базові витрати', reply_markup=client_btns.back_to_main_btn)
                await state.finish()

        except:
            await message.answer('Відповідь повинна бути у числовому форматі',
                                 reply_markup=client_btns.back_to_main_btn)

    if check_type_and_comparison:
        await db.set_budget(state)
        await message.answer('✅ Ваш місяний бюджет оновленно:\n\n'
                             f'    - загальний дохід за місяць: {data["total_income"]} грн\n'
                             f'    - місячна сумму базових витрат: {data["month_planing_base_expenses"]} грн\n\n'
                             f'🔐 Надано доступ до перегляду статистики 📈 ваших витрат:\n\n'
                             f' /today - за сьогодні\n'
                             f' /month - за поточний місяць', reply_markup=client_btns.static_and_back_main_menu)
        await state.finish()


async def cancel_handler_state_inline_btn(callback: types.CallbackQuery, state: FSMContext):
    """
    Cancellation of filling out the budget form
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.answer('ок, форма заповнення бджету скасована!', reply_markup=client_btns.back_to_main_btn)
    await callback.answer('ок, форма скасована!', show_alert=True)


def register_handlres_budjet(dp: Dispatcher):
    """register our funcs to handlers of set budjet story"""
    dp.register_message_handler(set_state_total_income, commands=['set_budget'], state=None)

    dp.register_callback_query_handler(cancel_handler_state_inline_btn, state="*")
    dp.register_message_handler(cancel_handler_state, state="*", commands='скасувати')
    # dp.register_message_handler(cancel_handler_state, Text(equals=['скасувати', 'отмена'], ignore_case=True), state="*")

    dp.register_message_handler(set_state_month_total_income, state=FSMBudjet.total_income)
    dp.register_message_handler(set_state_month_planing_base_expenses, state=FSMBudjet.month_planing_base_expenses)
