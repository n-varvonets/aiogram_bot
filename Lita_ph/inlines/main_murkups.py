from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import app.config as conf

btn_url_channel = InlineKeyboardButton(text="Channel", url=conf.CHANNEL_URL)
channel_menu = InlineKeyboardMarkup(row_width=1)
channel_menu.insert(btn_url_channel)


