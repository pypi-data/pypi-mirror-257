"""Generic way to send a RabbitMQ message."""

# Python modules
import json

# 3rd Party libraries
import pika
from dotenv import dotenv_values

RABBITMQ_HOST = dotenv_values().get("RABBITMQ_HOST")
RABBITMQ_PORT = dotenv_values().get("RABBITMQ_PORT")
RABBITMQ_VIRTUAL_HOST = dotenv_values().get("RABBITMQ_VIRTUAL_HOST")
RABBITMQ_USERNAME = dotenv_values().get("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = dotenv_values().get("RABBITMQ_PASSWORD")


def send_message(exchange_name, body, routing_key="") -> bool:
    """Send a message to RabbitMQ."""
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        virtual_host=RABBITMQ_VIRTUAL_HOST,
        credentials=credentials,
        connection_attempts=5,
        retry_delay=1,
    )

    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.basic_publish(
            exchange=exchange_name, routing_key=routing_key, body=json.dumps(body)
        )

        connection.close()

        return True
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error sending message to {exchange_name}")

    return False
