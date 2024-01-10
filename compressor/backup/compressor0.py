import io
import pika
import base64
from PIL import Image


def compress_image(image_data, quality=20):
    """
    Compresses the image to the specified quality.
    :param image_data: The binary data of the image.
    :param quality: Quality of the compressed image (1-100).
    :return: Compressed image data.
    """
    # Open the image from binary data
    image = Image.open(io.BytesIO(image_data))
    # Compress the image
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=quality)
    return buffer.getvalue()

def on_message_received(ch, method, properties, body):
    """
    Callback function that is called when a message is received.
    :param ch: Channel object.
    :param method: Method frame.
    :param properties: Properties frame.
    :param body: Received message body.
    """
    print("Received an image for compression.")
    # Decode the image from base64
    image_data = base64.b64decode(body)
    # Compress the image
    compressed_data = compress_image(image_data)
    # TODO: Send the compressed data back or save it
    print("Image compressed and processed.")

# Set up RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Assuming a queue named 'image_queue'
channel.queue_declare(queue='image_queue')

# Start consuming messages from the queue
channel.basic_consume(queue='image_queue', on_message_callback=on_message_received, auto_ack=True)
print('Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()

# def test_compression():
#     with open("woman.jpg", "rb") as image_file:
#         image_data = image_file.read()
#         compressed_data = compress_image(image_data)
#         # Save or display the compressed image for verification
#         with open("compressed_W.jpg", "wb") as compressed_file:
#             compressed_file.write(compressed_data)
#
# # Call this function for testing
# test_compression()