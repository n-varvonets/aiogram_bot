from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


welcome_btns = InlineKeyboardMarkup()\
    .row(
        InlineKeyboardButton(text=f'останні мої витрати', callback_data=f'/expenses'),
        InlineKeyboardButton(text=f'задати місячний бюджет', callback_data=f'/set_budget')
    ).row(
        InlineKeyboardButton(text=f'статистика за сьогодні', callback_data=f'/today'),
        InlineKeyboardButton(text=f'статистика за поточний місяць', callback_data=f'/month')
    ).row(
        InlineKeyboardButton(text=f'категорії витрат', callback_data=f'/categories'),
        InlineKeyboardButton(text=f'інфо', callback_data=f'/help')
    )