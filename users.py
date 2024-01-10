import sqlite3
from auth_utils import hash_password, check_password
from db import db_connect


class Users:
    @staticmethod
    def insert_user(username, password, profile_info=""):
        try:
            connection, cursor = db_connect()
            hashed_password = hash_password(password)
            cursor.execute("INSERT INTO Users (username, password, profile_info) VALUES (?, ?, ?)",
                           (username, hashed_password, profile_info))
            connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
            print("Username already exists. Please choose a different username.")
            return
        finally:
            connection.close()

    @staticmethod
    def login_user(username, password):
        try:
            connection, cursor = db_connect()
            cursor.execute("SELECT password FROM Users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result and check_password(result[0], password):
                print("Login successful.")
                return True
            else:
                return False
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
            print("Login failed.")
        finally:
            connection.close()
