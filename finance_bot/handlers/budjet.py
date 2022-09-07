from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher import Dispatcher


class FSMBudjet(StatesGroup):
    """
    В данном классе будет 2 состояния...
    """
    total_income = State()
    month_planing_base_expenses = State()


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

            if tuple(data.values())[0] > tuple(data.values())[
                1]:  # проверка на то указал ли клиент верно... а именно установил ли он месячньіх доход больше числа базовьіх растрат
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


def register_handlres_budjet(dp: Dispatcher):
    pass