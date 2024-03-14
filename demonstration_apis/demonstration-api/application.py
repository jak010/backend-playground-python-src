from fastapi import FastAPI

from src.api.member_router import api_router
from src.api.member_many_to_one_router import api_router_many_to_one
from src.api.member_value_object_router import api_router_value_object
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
        self.app.include_router(api_router_value_object)
        self.app.include_router(api_router_many_to_one)

        return self.app


demoapplication = DemonstrationApplication()
