from fastapi import FastAPI

from src.router import api_router
from src.concurrency_router import concurrency_router
from settings.dev import patch_ioc


class DemonstrationApplication:
    app = FastAPI(
        title="API Demonstration Server"
    )

    def __call__(self, *args, **kwargs):
        # conatiner patch
        patch_ioc()

        self.app.include_router(api_router)
        self.app.include_router(concurrency_router)

        return self.app


demoapplication = DemonstrationApplication()
