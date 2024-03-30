from fastapi import FastAPI

from settings.dev import patch_ioc
from src import backgrounds
from src.api.concurrency_lock_test import *
from src.api.relation_test import *
from src.api.router_v2.index_router import index_router_v1
from src.utils import start_mapper


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

        # router test
        self.app.include_router(index_router_v1)

        # Redis Lock Test
        self.app.include_router(concurrency_lock_test_router)

        # Background Task(with Thread)
        threads = [backgrounds.OtherBackgroundProcessThread()]
        for th in threads:
            th.start()

        return self.app


demoapplication = DemonstrationApplication()
