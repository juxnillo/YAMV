import sqlite3
from contextlib import contextmanager

# -- Constante --
DB_PATH = "database/collection.db"

CREATE_MEDIA_TABLE = """
    CREATE TABLE IF NOT EXISTS  media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT,
        genre TEXT,
        year INTEGER,
        image TEXT,
        rating INTEGER
    )
"""


@contextmanager
def get_connection():
    connection = sqlite3.connect(DB_PATH)
    try:
        yield connection
    finally:
        connection.close()


def create_table():
    with get_connection() as connection:
        with connection:
            connection.execute(CREATE_MEDIA_TABLE)


def add_media(title, media_type, genre, year, image, rating):
    with get_connection() as connection:
        with connection:
            connection.execute(
                """
              INSERT INTO media (title, type, genre, year, image, rating)
              VALUES (?, ?, ?, ?, ?, ?)
              """,
                (title, media_type, genre, year, image, rating),
            )


def get_media():
    with get_connection() as connection:
        cursor = connection.execute("SELECT * FROM media")
        return cursor.fetchall()


def delete_media(media_id):
    with get_connection() as connection:
        with connection:
            connection.execute("DELETE FROM media WHERE id = ?", (media_id,))
