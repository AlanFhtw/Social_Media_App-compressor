import sqlite3
import base64
import pika
import time
import threading  # Import the threading module
from db import db_connect


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
    def send_image_to_queue(image_path, queue_name="image_queue"):
        """
        Sends an image to the specified RabbitMQ queue for compression.
        """
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        encoded_data = base64.b64encode(image_data).decode('utf-8')

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.basic_publish(exchange='', routing_key=queue_name, body=encoded_data)
        connection.close()

    @staticmethod
    def listen_for_response(queue_name='response_queue', timeout=5):
        """
        Listens for a response message in the specified queue with a timeout.
        """

        def callback(ch, method, properties, body):
            global response_message
            response_message = body
            ch.stop_consuming()

        def consume():
            global response_message
            response_message = None

            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue=queue_name)
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

            channel.start_consuming()
            connection.close()

        global response_message
        response_message = None

        # Start the consumer in a separate thread
        consumer_thread = threading.Thread(target=consume)
        consumer_thread.start()

        # Wait for the response or timeout
        consumer_thread.join(timeout)
        if consumer_thread.is_alive():
            # Stop consuming if the thread is still alive after the timeout
            consumer_thread._stop()  # Use ._stop() cautiously as it's an internal method

        return response_message

    @staticmethod
    def insert_post(post):
        connection, cursor = db_connect()
        try:
            # Send image to the queue for compression
            Posts.send_image_to_queue(post['image'])

            # Listen for a response with the compressed image
            compressed_image_response = Posts.listen_for_response()
            if compressed_image_response:
                # Process the response (e.g., decode base64 image)
                compressed_image = base64.b64decode(compressed_image_response)
                # Insert post with compressed image
                cursor.execute("INSERT INTO Posts (user_id, content, image) VALUES (?, ?, ?)",
                               (post["user_id"], post["content"], compressed_image))
                connection.commit()
            else:
                print("Did not receive compressed image in time")
                return  # Exit if compressed image is not received

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
