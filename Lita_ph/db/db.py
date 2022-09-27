import os
from typing import Dict, List, Tuple
import time
import sqlite3

PATH_TO_DB_SQL = "/home/nick/PycharmProjects/iogram_bot/Lita_ph/db/create_db_lita.sql"  # for local


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self._check_db_exists()

    def _init_db(self):
        """Инициализирует БД"""
        with open(PATH_TO_DB_SQL, "r") as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.connection.commit()

    def _check_db_exists(self):
        """Проверяет, инициализирована ли БД, если нет — инициализирует"""
        self.cursor.execute("SELECT name FROM sqlite_master "
                            "WHERE type='table' AND name='users'")
        table_exists = self.cursor.fetchall()
        if table_exists:
            return print('Existing DB is connected')

        self._init_db()
        print('Was created new DB from sql file')

    def user_exist(self, user_id):
        """check if user exist at current time"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ).fetchall()
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users ('user_id') VALUES (?)", (user_id,))

    def _is_mute(self, user_id):
        """
        If the user is mute will return True
        :param user_id:
        :return: bool
        """
        with self.connection:
            user_mute_status = self.cursor.execute("SELECT mute_time FROM users WHERE user_id = ?", (
                user_id,)).fetchone()
            return int(user_mute_status[0]) >= int(time.time())

    def _set_mute(self, user_id, mute_time):
        """
        set mute on user.
        :param mute_time: in seconds
        """
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET mute_time = ? WHERE user_id = ?",
                (int(time.time() + mute_time), user_id)
            )  # to current time adding mute time in sec


