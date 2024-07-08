from fastapi import FastAPI
from sqladmin import Admin

from admin.view import UserAmdinView
from settings.dev import get_engine, patch_ioc
from src.api.asynctic.endpoints import asyncio_router

from src.api.concurrency_lock_test import *
from src.api.concurrency_router import nonblock_router
from src.api.relation_test import *
from src.api.router_v2.index_router import index_router_v1
from src.api.proxysql.proxysql_controller import proxysql_api_router
from src.api.mongodb.endpoints import mongodb_router
from src.utils import start_mapper
from src.api.fileupload_example.fileupload_api import fileupload_router


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
        self.app.include_router(proxysql_api_router)

        # router test
        self.app.include_router(index_router_v1)

        # Redis Lock Test
        self.app.include_router(concurrency_lock_test_router)

        # MongoDB Test
        self.app.include_router(mongodb_router)

        # non block
        self.app.include_router(nonblock_router)

        # Asyncio Test
        self.app.include_router(asyncio_router)

        # File Upload Test
        self.app.include_router(fileupload_router)

        # Background Task(with Thread)
        # threads = [backgrounds.OtherBackgroundProcessThread()]
        # for th in threads:
        #     th.start()

        return self.app


class DemonstrationAdminApplication:

    def __init__(self, app, engine, authenticate=None):
        self.admin_app = Admin(app, engine)

    def add_view(self, model):
        self.admin_app.add_view(model)


demoapplication = DemonstrationApplication()

# Admin Setting
demoadminapplication = DemonstrationAdminApplication(
    app=demoapplication.app,
    engine=get_engine(),
    authenticate=None
)
demoadminapplication.add_view(UserAmdinView)
