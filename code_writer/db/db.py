import os
from typing import Dict, List, Tuple
import time
import sqlite3

PATH_TO_DB_SQL = "/home/nick/PycharmProjects/iogram_bot/code_writer/db/createdb.sql"  # for local


# conn = sqlite3.connect()

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self._check_db_exists()

    def _init_db(self):
        """Инициализирует БД"""
        # path_to_db_sql = "/home/db/createdb.sql"  # for docker
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

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))

    def user_exist(self, user_id):
        """check if user exist at current time"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM 'users' WHERE 'user_id' = ?", (user_id,)
            ).fetchall()  # получаем все поля, которое поле user_id равно тому user_id, которое мы передали
            return bool(len(result))  # прикольный возрат тру/фолса, от результата длины списка на истинность

    def set_nickname(self, user_id, nickname):
        """т.к. никнейм в бд может быть пустым, то по айди - его можно установить или отредаккитровать"""
        with self.connection:
            # return self.cursor.execute("INSERT INTO 'users' ('nickname') WHERE 'user_id' = ? VALUES (?)",
            #                            (user_id, nickname))
            return self.cursor.execute("UPDATE users SET nickname = ? WHERE user_id = ?", (str(nickname), user_id))

    def get_sign_up_stage(self, user_id):
        """define stage registration of user"""
        with self.connection:
            result = self.cursor.execute("SELECT sign_up FROM users WHERE user_id = ?", (
                user_id,)).fetchall()  # user_id - олжен быть без скобок, а то ошибки будут и sign_up без скобок, а то возьмет только названия поля, а не его значениме
            for row in result:
                sign_up = str(row[0])
            return sign_up

    def set_sign_up_stage(self, user_id, sign_up):
        """define stage registration of user"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET sign_up = ? WHERE user_id = ?", (str(sign_up), user_id))

    def get_nickname(self, user_id):
        """define stage registration of user"""
        with self.connection:
            result = self.cursor.execute("SELECT nickname FROM users WHERE user_id = ?", (
                user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname

    def set_time_subscription(self, user_id, time_sub):
        """set time subscription of user"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET time_sub = ? WHERE user_id = ?", (str(time_sub), user_id))

    def get_time_subscription(self, user_id):
        """get subscription of user"""
        with self.connection:
            result = self.cursor.execute("SELECT time_sub FROM users WHERE user_id = ?", (
                user_id,)).fetchall()
            for row in result:
                if row[0] is not None:
                    time_sub = int(row[0])
            return time_sub

    def get_time_subscription_bool(self, user_id):
        """get subscription of user"""
        with self.connection:
            result = self.cursor.execute("SELECT time_sub FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                if row[0] is not None:
                    time_sub = row[0]


            if int(time_sub) > (time.time()):
                # если время подписки  больше нынешнего - возращаем тру - т.е. подписка есть
                return True
            else:
                return False
