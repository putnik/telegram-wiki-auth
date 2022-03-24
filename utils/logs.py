# -*- coding: utf-8 -*-

from utils.db import execute_query


def init_logs_table():
    execute_query('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            tg_chat INTEGER NOT NULL,
            tg_id INTEGER NOT NULL,
            tg_name CHAR(255) NOT NULL,
            action CHAR(50) NOT NULL,
            value CHAR(255) NOT NULL,
            text TEXT NOT NULL
        )
    ''')


def log(message, action: str, value: str = ''):
    query = '''
        INSERT INTO logs (tg_chat, tg_id, tg_name, action, value, text)
        VALUES (%d, %d, '%s', '%s', '%s', '%s')
    ''' % (
        message.chat.id,
        message.from_user.id,
        message.from_user.username,
        action,
        value,
        message.text
    )
    execute_query(query)


def log_web(action: str, value: str = '', text: str = '', tg_id: int = 0):
    query = '''
        INSERT INTO logs (tg_chat, tg_id, tg_name, action, value, text)
        VALUES (0, %d, '', '%s', '%s', '%s')
    ''' % (
        tg_id,
        action,
        value,
        text
    )
    execute_query(query)
