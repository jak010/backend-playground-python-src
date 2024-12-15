import asyncio
import time

from fastapi.concurrency import run_in_threadpool


class LegacyDomainEventListener:

    async def handle_event(self):
        while True:
            await asyncio.sleep(0.1)
            print("1")
