import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.application.event_listener import LegacyDomainEventListener


@asynccontextmanager
async def lifespace(app):
    print("Start")

    e = LegacyDomainEventListener(app)
    asyncio.create_task(e.handle_event())

    yield


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
