# -*- coding: utf-8 -*-

from utils.db import execute_query, fetch_all, fetch_value


def init_users_table():
    execute_query('''
        CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER PRIMARY KEY NOT NULL,
            tg_name CHAR(255) NOT NULL,
            wiki_name CHAR(255) NOT NULL
        )
    ''')


def get_all_ids():
    rows = fetch_all("SELECT tg_id FROM users")
    return [row[0] for row in rows]


def get_username(tg_id: int):
    return fetch_value("SELECT wiki_name FROM users WHERE tg_id = %d" % tg_id)


def create_user(tg_id: int, tg_name: str, wiki_name: str):
    query = "INSERT INTO users (tg_id, tg_name, wiki_name) VALUES (%d, '%s', '%s')"
    execute_query(query % (tg_id, tg_name, wiki_name))


def delete_user(tg_id: int):
    execute_query("DELETE FROM users WHERE tg_id = %d" % tg_id)
