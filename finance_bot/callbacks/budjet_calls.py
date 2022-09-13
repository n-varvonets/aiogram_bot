from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram import types
from inlines import budjet_btns, client_btns
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.budjet import  FSMBudjet


async def set_budjet_cb(callback: types.CallbackQuery):
    """Start filling the budget form via StateGroup"""
    await FSMBudjet.total_income.set()
    await callback.message.answer('Вкажіть Ваш загальний дохід за місяць, грн,\n\n'
                         '➡️  наприклад: 15000 чи 15_000', reply_markup=budjet_btns.cancel_btn)
    await callback.answer()


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


def register_budjet_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(set_budjet_cb, text='set_budget_cb_btn')
    dp.register_callback_query_handler(cancel_handler_state_inline_btn, state="*")
