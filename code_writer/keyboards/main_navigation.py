from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# --- Main menu ---
b1 = KeyboardButton('👤PROFILE')
b2 = KeyboardButton('❤️SUBSCRIPTION')
b3 = KeyboardButton('💰 COINS')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)

# btn_only_for_subscribed = KeyboardButton('✅️SUBSCRIDED FUNC')
# main_menu.add(b1, b2).add(btn_only_for_subscribed)

main_menu.add(b1, b2).add(b3)


# --- Subscribe inline btn ---
sub_inline_markup = InlineKeyboardMarkup(row_width=1)
btn_sub_month = InlineKeyboardButton(text="Month - 50 UAH", callback_data='submonth')
sub_inline_markup.insert(btn_sub_month)


# --- Subscribe inline btn ---
btn_bitcoin = InlineKeyboardButton(text='Bitcoin', callback_data='cc_bitcoin')
btn_litecoin = InlineKeyboardButton(text='Litecoin', callback_data='cc_litecoin')
btn_dogecoin = InlineKeyboardButton(text='Dogecoin', callback_data='cc_dogecoin')

crypto_list = InlineKeyboardMarkup(row_width=1)
crypto_list.insert(btn_bitcoin)
crypto_list.insert(btn_litecoin)
crypto_list.insert(btn_dogecoin)
