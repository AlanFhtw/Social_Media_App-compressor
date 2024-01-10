import sqlite3
from db import db_connect
import base64


class Posts:
    @staticmethod
    def _convert_img_to_base64(filename):
        with open(filename, 'rb') as file:
            binary_data = file.read()
            base64_data = base64.b64encode(binary_data).decode('utf-8')
        return base64_data

    @staticmethod
    def _convert_base64_to_binary(base64_data):
        binary_data = base64.b64decode(base64_data)
        return binary_data

    @staticmethod
    def insert_post(post):
        connection, cursor = db_connect()
        try:
            base64_image = Posts._convert_img_to_base64(post['image'])

            cursor.execute("INSERT INTO Posts (user_id, content, image) VALUES (?, ?, ?)",
                           (post["user_id"], post["content"], base64_image))
            connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        finally:
            connection.close()

    @staticmethod
    def get_latest_post():
        connection, cursor = db_connect()
        try:
            cursor.execute("SELECT * FROM Posts ORDER BY created_at DESC LIMIT 1")
            post = cursor.fetchone()

            if post:
                post_image_base64 = post[3]
                post_image_binary = Posts._convert_base64_to_binary(post_image_base64)
                post = post[:3] + (post_image_binary,) + post[4:]

            return post
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
            print("There seems to be no posts yet in the database.")
        finally:
            connection.close()

    @staticmethod
    def get_all_posts():
        try:
            connection, cursor = db_connect()
            cursor.execute("SELECT * FROM Posts ORDER BY created_at DESC")
            cursor.fetchall()
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        finally:
            connection.close()

    @staticmethod
    def add_comment(comment):
        connection, cursor = db_connect()
        try:
            cursor.execute("INSERT INTO Comments (user_id, post_id, content) VALUES (?, ?, ?)",
                           (comment["user_id"], comment["post_id"], comment["content"]))
            connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error adding comment: {e}")
        finally:
            connection.close()

    @staticmethod
    def get_comments_for_post(post_id):
        connection, cursor = db_connect()
        try:
            cursor.execute("SELECT * FROM Comments WHERE post_id = ? ORDER BY created_at", (post_id,))
            comments = cursor.fetchall()
            return comments
        except sqlite3.IntegrityError as e:
            print(f"Error getting comments: {e}")
        finally:
            connection.close()

    @staticmethod
    def add_like(like):
        connection, cursor = db_connect()
        try:
            cursor.execute("INSERT INTO Likes (user_id, post_id) VALUES (?, ?)",
                           (like["user_id"], like["post_id"]))
            connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error adding like: {e}")
        finally:
            connection.close()

    @staticmethod
    def get_likes_for_post(post_id):
        connection, cursor = db_connect()
        try:
            cursor.execute("SELECT * FROM Likes WHERE post_id = ? ORDER BY created_at", (post_id,))
            likes = cursor.fetchall()
            return likes
        except sqlite3.IntegrityError as e:
            print(f"Error getting likes: {e}")
        finally:
            connection.close()
