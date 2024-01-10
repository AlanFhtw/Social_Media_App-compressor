import sqlite3

db = 'app.db'


def db_connect():
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    return connection, cursor


def create_tables():
    connection, cursor = db_connect()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Users ("
        "id INTEGER PRIMARY KEY,"
        "username VARCHAR(50) NOT NULL UNIQUE,"
        "password VARCHAR(20) NOT NULL,"
        "profile_info VARCHAR(255));")

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Posts ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "user_id INT NOT NULL,"
        "content TEXT NOT NULL,"
        "image BLOB,"
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (user_id) REFERENCES Users(id));")

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Comments ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "user_id INT NOT NULL,"
        "post_id INT NOT NULL,"
        "content TEXT NOT NULL,"
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (user_id) REFERENCES Users(id),"
        "FOREIGN KEY (post_id) REFERENCES Posts(id));")

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Likes ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "user_id INT NOT NULL,"
        "post_id INT NOT NULL,"
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (user_id) REFERENCES Users(id),"
        "FOREIGN KEY (post_id) REFERENCES Posts(id));")

    connection.commit()
    connection.close()
