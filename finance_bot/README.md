В переменных окружения надо проставить API токен бота, а также адрес proxy и логин-пароль к ней.

`TELEGRAM_API_TOKEN` — API токен бота

`TELEGRAM_ACCESS_ID` — ID Telegram аккаунта, от которого будут приниматься сообщения (сообщения от остальных аккаунтов игнорируются)

Заллить данньіе в бд из файла .sql

```
sqlite3 db.db < createdb.sql
```

Так же если нет папки db в оснонов путе к данному проекту, то нужно ее будет создать, что бьі бот там создал .db


Использование с Docker показано ниже. Предварительно заполните ENV переменные, указанные выше, в Dockerfile, а также в команде запуска укажите локальную директорию с проектом вместо `local_project_path`. SQLite база данных будет лежать в папке проекта `db/finance.db`.

```
docker build -t tgfinance ./
docker run -d --name tg -v /local_project_path/db:/home/db tgfinance
```

Чтобы войти в работающий контейнер:

```
docker exec -ti tg bash
```

Войти в контейнере в SQL шелл:

```
docker exec -ti tg bash
sqlite3 /home/db/finance.db
```

Запустить на сервере прилажуху нужно создать демон(как пример cwbot.service) по роуту:

```
/etc/systemd/system/
чtрез vim cwbot.service и вписать туда команды что в примере локального проекта
```
Добавляем наш сервис в автозапуск и стартуем его: 

```
sudo systemctl enable cwbot
sudo systemctl start cwbot
```
Посмотреть логи бота

```
journalctl -u cwbot.service
```























































":{L ?>['po/;.lmnj hb]'[po;lkijuyh
```


Bot-opening for about and description:

Привіт, я бот помічник компанії "Мамкін розробник"
Моя ціль - допомоти Вам вести облік своїх фінансів 🤓

Збережу всі Ваші витрати, які автоматично поділю по категоріям і проведу відповідну базову аналітику 🧐

