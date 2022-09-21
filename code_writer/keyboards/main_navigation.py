from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# --- Main menu ---
b1 = KeyboardButton('👤PROFILE')
b2 = KeyboardButton('❤️SUBSCRIPTION')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)

btn_only_for_subscribed = KeyboardButton('✅️SUBSCRIDED FUNC')


main_menu.add(b1, b2).add(btn_only_for_subscribed)


# --- Subscribe inline btn ---
sub_inline_markup = InlineKeyboardMarkup(row_width=1)
btn_sub_month = InlineKeyboardButton(text="Month - 50 UAH", callback_data='submonth')
sub_inline_markup.insert(btn_sub_month)