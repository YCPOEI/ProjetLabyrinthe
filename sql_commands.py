# -*- coding: utf-8 -*-
import sqlite3


def creation_historique():
    conn = None
    try:
        conn = sqlite3.connect("historique.sqlite")
        cur = conn.cursor()
        cur.execute(
            """ DROP TABLE IF EXISTS historique
                    """
        )
        cur.execute(
            """ CREATE TABLE IF NOT EXISTS historique(
                    id integer PRIMARY KEY,
                    entree TEXT);
                    """
        )
        return conn
    except sqlite3.Error as e:
        print(e)


def add_task(conn, task):
    sql = """ INSERT INTO historique(entree)
              VALUES(?) """
    cur = conn.cursor()
    print("task:", task)
    task = (task,)
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid


def select(conn):
    sql = """ SELECT * FROM historique """
    cur = conn.cursor()
    result = cur.execute(sql)
    conn.commit()
    print("Result:", result)
    rows = cur.fetchall()
    return rows


def close(conn):
    conn.close()
