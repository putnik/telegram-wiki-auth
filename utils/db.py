# -*- coding: utf-8 -*-

from sqlite3 import connect

DB_NAME = 'wiki.db'


def execute_query(query: str):
    # print(query)
    con = connect(DB_NAME)
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    con.close()


def fetch_all(query: str):
    # print(query)
    con = connect(DB_NAME)
    cursor = con.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()
    con.close()

    return rows


def fetch_one(query: str):
    # print(query)
    con = connect(DB_NAME)
    cursor = con.cursor()

    cursor.execute(query)
    row = cursor.fetchone()
    con.close()

    return row


def fetch_value(query: str):
    row = fetch_one(query)
    if row is None:
        return None
    return row[0]
