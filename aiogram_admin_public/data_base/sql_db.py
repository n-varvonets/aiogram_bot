import sqlite3 as sql
from create_bot import bot


def sql_start():
    """
    Для примера возьмем sql3 - файловая бд в оперативной памяти.
    Данная функция подключения к бд будет вьізоваться перед стартом пулинга нашим ботом в нашем основном скрипте
    """
    global base, cur
    base = sql.connect(
        "my_telegram_ product.db")  # если такого файла не будет - он создаться, если будет, то будет записьівать в него
    cur = base.cursor()
    if base:  # если успешно подключились к бд, то вьіводим статус в консоль
        print('Data base connected OK!')
    base.execute(
        'CREATE TABLE IF NOT EXISTS clients_data( img TEXT, name TEXT PRIMARY_KEY, description TEXT, age FLOAT)')  # PRIMARY_KEY - уникальное название
    base.commit()


async def sql_add_command(state):
    """получаем наше состояние формьі и при открьівании там будет словарь с нашими значениями для ИНСЕРТА записи"""
    async with state.proxy() as data:
        cur.execute('INSERT INTO clients_data VALUES (?, ?, ?, ?)', tuple(data.values()))
        print(f'The product was processed successfully {data["name"]}')
        base.commit()


async def sql_read_all_clients(message):
    for ret in cur.execute('SELECT * FROM clients_data').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'Имя: {ret[1]}\nОписание: {ret[2]}\nage {ret[-1]}')


async def sql_fetch_all_clients():
    return cur.execute('SELECT * FROM clients_data').fetchall()


async def sql_delete_client(client):
    cur.execute('DELETE FROM clients_data WHERE name == ?', (client,))
    base.commit()
