import sqlite3
from sqlite3.dbapi2 import Cursor


def connect():
    return sqlite3.connect("database/collection.db")


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
        rating INTEGER
    )
    """)

    connection.commit()
    connection.close()


def add_media(title, media_type, genre, year, image, rating):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO media (title, type, genre, year, image, rating)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (title, media_type, genre, year, image, rating),
    )

    connection.commit()
    connection.close()


def get_media():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM media")
    data = cursor.fetchall()

    connection.close()
    return data

def delete_media(media_id):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM media WHERE id = ?", (media_id,))

    connection.commit()
    connection.close()
