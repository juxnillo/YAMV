import sqlite3


def connect():
    return sqlite3.connect("collection.db")


def create_table():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS  media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT,
            genre TEXT,
            year INTEGER,
            image TEXT,
            rating INTEGER,
        )
    """)

    connection.commit()
    connection.close()
