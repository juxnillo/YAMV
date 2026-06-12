from database.db import create_table, get_media, add_media

if __name__ == "__main__":
    create_table()
    add_media("One Piece", "Anime", "Shonen", 1999, "images/op.jpg", 9)
    print(get_media())
