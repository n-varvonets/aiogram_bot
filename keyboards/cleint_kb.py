from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Режим_роботи')
b2 = KeyboardButton('/Місце_знаходження')
b3 = KeyboardButton('Меню')
# так же можно поделиться своим контактом и отправить свое местоположение:
b4 = KeyboardButton('поделиться своим контактом', request_contact=True)
b5 = KeyboardButton('отправить свое местоположение', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

# kb_client.add(b1).add(b2).add(b3)  # add - метод добавляет кнопку КАЖДИЙ РАЗ с НОВОЙ СТРОКИ
# kb_client.add(b1).add(b2).insert(b3)  # insert - метод добавляет кнопку  КАЖДИЙ РАЗ в ту же строку(если есть место)
# kb_client.row(b1, b2, b3)  # row - метод добавляет все кнопки в одну строку

kb_client.add(b1).add(b2).add(b3).row(b4, b5)
