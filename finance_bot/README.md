In the environment variables you must put the API token of the bot. Ask father bot from telegram.

`TELEGRAM_API_TOKEN` — API bot token

`TELEGRAM_ACCESS_ID` — Telegram account ID from which messages will be received (messages from other accounts are ignored)

Fill data into the database from a .sql file
```
sqlite3 db.db < createdb.sql
```

Так же если нет папки db в оснонов путе к данному проекту, то нужно ее будет создать, что бьі бот там создал .db


Use with Docker is shown below. Fill in the ENV variables above in the Dockerfile beforehand, and also specify the local directory with the project instead of `local_project_path` in the start command. SQLite database will lie in the project folder `db/finance.db`.

```
docker build -t ur_finance_bot ./
docker run -d --name ufb ur_finance_bot
```

* useful add docker info:
- if our image is now running in a running container;
- to view if our image is running now; - the history of all running clients
- see console logs of running image
- delete old unwanted image
- go inside the running container

- kill process(including solving err - permition denied: docker.socket)

```
docker ps
docker ps -a
docker logs <CONTAINER ID>
docker rm ufb
docker exec -ti ufb bash

sudo systemctl stop docker.socket
sudo service docker restart
```

Opening for bot about and description:

Привіт, я бот помічник компанії "Мамкін розробник"
Моя ціль - допомоти Вам вести облік своїх фінансів 🤓

Збережу всі Ваші витрати, які автоматично поділю по категоріям і проведу відповідну базову аналітику 🧐




