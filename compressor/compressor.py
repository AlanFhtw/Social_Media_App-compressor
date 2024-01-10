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

    print("Image compressed.")

    # After compression, send a response
    response = base64.b64encode(compressed_data).decode('utf-8')  # or a reference to the stored image
    ch.basic_publish(exchange='', routing_key='response_queue', body=response)
    print("Compressed image and sent response.")

    # Save the compressed image
    # with open("compressed_w.jpeg", "wb") as compressed_file:
    #     compressed_file.write(compressed_data)
    # print("Image compressed and saved as compressed_w.jpeg.")

def send_test_message(queue_name, image_path):
    """
    Sends a test message (encoded image) to the specified queue.
    :param queue_name: Name of the queue to publish the message.
    :param image_path: Path to the image file to be sent.
    """
    # Read and encode the image
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    encoded_data = base64.b64encode(image_data)

    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Send the message
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=encoded_data)
    print(f"Sent an image to queue {queue_name}")

    # Close the connection
    connection.close()

def test_compression():
    with open("woman.jpg", "rb") as image_file:
        image_data = image_file.read()
        compressed_data = compress_image(image_data)
        # Save or display the compressed image for verification
        with open("compressed_woman.jpg", "wb") as compressed_file:
            compressed_file.write(compressed_data)

# Uncomment the following line to test compression locally
# test_compression()

# Set up RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


# Declare the queue with 'durable' set to True
channel.queue_declare(queue='image_queue', durable=True)

# Start consuming messages from the queue
channel.basic_consume(queue='image_queue', on_message_callback=on_message_received, auto_ack=True)
print('Waiting for messages. To exit, press CTRL+C')

# Uncomment the following line to send a test message through RabbitMQ
# send_test_message("image_queue", "woman.jpg")

channel.start_consuming()


