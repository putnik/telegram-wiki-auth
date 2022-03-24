# -*- coding: utf-8 -*-

from utils.db import execute_query, fetch_one


def init_states_table():
    execute_query('''
        CREATE TABLE IF NOT EXISTS states (
            state CHAR(48) PRIMARY KEY,
            tg_id INTEGER NOT NULL,
            tg_name CHAR(255) NOT NULL,
            time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            is_used INTEGER NOT NULL DEFAULT 0
        )
    ''')


def create_state(state: str, tg_id: int, tg_name: str):
    query = "INSERT INTO states (state, tg_id, tg_name) VALUES ('%s', %d, '%s')" % (
        state,
        tg_id,
        tg_name
    )
    execute_query(query)


def get_by_state(state: str, is_used: int = 0):
    row = fetch_one('''
        SELECT tg_id, tg_name
        FROM states
        WHERE state = '%s'
            AND time >= DATETIME('now', '-600 seconds')
            AND is_used = %d
    ''' % (state, is_used))
    if row is None:
        return None, None
    return row[0], row[1]


def mark_state_used(state: str):
    execute_query("UPDATE states SET is_used = 1 WHERE state = '%s'" % state)
