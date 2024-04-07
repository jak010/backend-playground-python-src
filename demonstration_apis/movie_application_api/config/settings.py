from abc import ABCMeta, abstractmethod
from typing import List

from dependency_injector.containers import DeclarativeContainer
from fastapi import FastAPI, APIRouter


class AbstractSetting(metaclass=ABCMeta):
    app: FastAPI

    def application(self, app: FastAPI):
        self.app = app

    @abstractmethod
    def adapter_patch(self, containers: List[DeclarativeContainer]): ...

    # @abstractmethod
    # def start_mappers(self): ...

    def include_routers(self, routers: List[APIRouter]):
        for router in routers:
            self.app.include_router(router)


class LocalSetting(AbstractSetting):

    def adapter_patch(self, containers):
        for container in containers:
            container.wire(modules=["src"])
