from db import db
import os

PATH_TO_DB_FILE = os.path.join("", "db/lita_ph.db")
my_orm = db.Database(PATH_TO_DB_FILE)
# LiqPay_TOKEN = '5488841036:AAHYQSXIms6gBnA2lejPcklZtKPbxj7UNdk'
API_BOT_TOKEN = '5488841036:AAHYQSXIms6gBnA2lejPcklZtKPbxj7UNdk'
ADMIN_ID = 402431758
CHANNEL_URL = 'https://t.me/Lita_healthcare'  # что бы пользователя попросить подписаться на канал
CHANNEL_ID = '@Lita_healthcare'  # id нашего канала
CHAT_ID = '@Lita_healthcare_chat'  # логин нашего телеграм чата

