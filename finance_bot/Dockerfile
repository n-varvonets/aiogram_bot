FROM python:3.8

WORKDIR /home

ENV TELEGRAM_API_TOKEN="5596636154:AAHi-yo6fKDzEyoV79oHvg4IrCo7iVy2rTQ"
ENV TELEGRAM_ACCESS_ID="40243175"

RUN pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3

COPY app/ /home/app/
COPY db/ /home/db/
COPY exceptions/ /home/exceptions/
COPY handlers/ /home/handlers/
COPY inlines/ /home/inlines/
COPY keyboards/ /home/keyboards/
COPY *.py /home/

# RUN sqlite3 /home/db/finance.db < /home/db/createdb.sql

ENTRYPOINT ["python", "server.py"]

