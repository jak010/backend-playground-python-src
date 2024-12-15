from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.application.event_listener import LegacyDomainEventListener
import asyncio
from fastapi.concurrency import run_in_threadpool
import anyio.to_thread


@asynccontextmanager
async def lifespace(app):
    print("Start")

    e = LegacyDomainEventListener()

    asyncio.create_task(e.handle_event())
    #
    # await run_in_threadpool(e.handle_event, 1200)

    # asyncio.create_task(
    #     await e.handle_event()
    # )

    yield
    print("End")


class GradualMigrationApplication:

    def __init__(self):
        self.app = FastAPI(
            title="Gradual Migration DSP API",
            description="Gradual Migration DSP API Document",
            lifespan=lifespace
        )

    def __call__(self, *args, **kwargs):
        from src.apis.index_router import index_router

        self.app.include_router(index_router)

        return self.app


application = GradualMigrationApplication()
