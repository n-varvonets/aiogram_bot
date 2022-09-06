from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# кнопки команд для админа
button_load = KeyboardButton("/Загрузить_клиента")
button_delete = KeyboardButton("/Удалить_клиента")
button_clients_catalog = KeyboardButton("get our clients")
button_cancel = KeyboardButton("/отмена")

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(button_load, button_cancel).row(button_clients_catalog, button_delete)
