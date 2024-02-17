from fastapi import FastAPI

from src.router import api_router


class DemonstrationApplication:
    app = FastAPI(
        title="API Demonstration Server"
    )

    def __call__(self, *args, **kwargs):
        self.app.include_router(api_router)

        return self.app


demoapplication = DemonstrationApplication()
