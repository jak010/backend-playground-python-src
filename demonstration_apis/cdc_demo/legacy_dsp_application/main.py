from fastapi import FastAPI

from config import mapper, container

from src.apis.index import index_router
from src.apis.user import legacy_user


class LegacyDSPApplication:
    containers = [container.SqlAlchemyConatiner()]

    def __init__(self):
        self.app = FastAPI(
            title="Legacy DSP API",
            description="Legacy DSP API Document"
        )

    def __call__(self, *args, **kwargs):
        mapper.start_mapper()

        for item in self.containers:
            item.wire(packages=["src"])

        self.app.include_router(index_router)
        self.app.include_router(legacy_user)

        return self.app


application = LegacyDSPApplication()
