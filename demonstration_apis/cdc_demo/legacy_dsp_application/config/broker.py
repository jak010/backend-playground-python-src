import json

import pika
from src.application.events.message import DomainMessage


class MessageQueuePublisher:
    EXCHANGE = 'legacy-topic'
    QUEUE_NAME = 'test-queue'
    ROUTING_KEY = 'test-queue'

    def __init__(self):
        self.credentials = pika.PlainCredentials(
            username="ruser",
            password="localpw"
        )
        self.paramaters = pika.ConnectionParameters(
            host="localhost",
            port=5673,
            virtual_host="legacy",
            credentials=self.credentials
        )

    def send(self, message: DomainMessage):
        connection = pika.BlockingConnection(self.paramaters)

        channel = connection.channel()
        channel.queue_declare(queue=self.QUEUE_NAME, durable=True)
        channel.basic_publish(
            exchange=self.EXCHANGE,
            routing_key=self.ROUTING_KEY,
            body=message.to_output_message(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        connection.close()
