import asyncio

import aio_pika
from aio_pika import connect_robust
from .broker import MessageQueueConsumer


class LegacyDomainEventListener:
    INTERVAL_SECONDS = 1 / 100

    def __init__(self, app):
        self.app = app

    async def handle_event(self):
        self.connection = await connect_robust(MessageQueueConsumer.get_connection())
        while True:
            await asyncio.sleep(self.INTERVAL_SECONDS)
            channel = await self.connection.channel()
            queue = await channel.declare_queue(
                MessageQueueConsumer.QUEUE_NAME.value,
                durable=True
            )
            await queue.consume(self.call_back)

            try:
                await asyncio.Future()
            finally:
                await self.connection.close()

    async def call_back(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        async with message.process():
            msg = message.body.decode()
            print(msg)
            await asyncio.sleep(self.INTERVAL_SECONDS)
