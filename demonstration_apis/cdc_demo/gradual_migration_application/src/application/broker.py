from enum import Enum


class MessageQueueConsumer(Enum):
    EXCHANGE = 'legacy-topic'
    QUEUE_NAME = 'test-queue'
    ROUTING_KEY = 'test-queue'

    @classmethod
    def get_connection(cls):
        return "amqp://ruser:localpw@localhost:5673/legacy"
