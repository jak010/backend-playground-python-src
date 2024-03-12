from fastapi import FastAPI

from src.api.member_router import api_router
from src.utils import start_mapper
from settings.dev import patch_ioc


class DemonstrationApplication:
    app = FastAPI(
        title="API Demonstration Server"
    )

    def __call__(self, *args, **kwargs):
        # conatiner patch
        patch_ioc()
        start_mapper()

        self.app.include_router(api_router)

        return self.app


demoapplication = DemonstrationApplication()
