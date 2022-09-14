from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('👤PROFILE')
b2 = KeyboardButton('❤️SUBSCRIPTION')


main_menu = ReplyKeyboardMarkup(resize_keyboard=True)

main_menu.add(b1, b2)
