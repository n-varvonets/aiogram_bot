from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


cancel_btn = InlineKeyboardMarkup()\
    .add(InlineKeyboardButton(
    text=f'скасувати заповененния бюджету', callback_data=f'скасувати'
))

