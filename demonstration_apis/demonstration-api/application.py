from fastapi import FastAPI

from src.api.relation_test import *
from src.api.concurrency_lock_test import *
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

        # Relation Test
        self.app.include_router(api_router)
        self.app.include_router(api_router_value_object)
        self.app.include_router(api_router_many_to_one)

        # Redis Lock Test
        self.app.include_router(concurrency_lock_test_router)

        return self.app


demoapplication = DemonstrationApplication()
