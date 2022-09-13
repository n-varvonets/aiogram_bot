import os
from typing import Dict, List, Tuple

import sqlite3

conn = sqlite3.connect(os.path.join("", "db/finance.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def update_daily_budjet(total_income: int, month_planing_base_expenses: int) -> None:
    """Оновлює таблицю денног ліміта витрат"""
    cursor.execute(
        f"insert into budget(total_income, month_planing_base_expenses) values ('{total_income}', {month_planing_base_expenses});")
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    # path_to_db_sql = "/home/db/createdb.sql"  # for docker
    path_to_db_sql = "/home/nick/PycharmProjects/iogram_bot/finance_bot/db/createdb.sql"  # for local
    with open(path_to_db_sql, "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


async def set_budget(state):
    """получаем наше состояние формьі и при открьівании там будет словарь с нашими значениями для ИНСЕРТА записи"""
    async with state.proxy() as data:
        cursor.execute(f"insert into budget(total_income, month_planing_base_expenses) values {tuple(data.values())}")
        conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='expense'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
