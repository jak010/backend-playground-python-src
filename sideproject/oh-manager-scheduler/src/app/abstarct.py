import datetime

from dependency_injector.wiring import Provide
from abc import ABCMeta
from src.config.container import DataBaseContainer

from typing import TypedDict


class AbstractCommandQuery(metaclass=ABCMeta):
    session = Provide[DataBaseContainer.session]


class AbstractLoaderDataType(TypedDict):
    id: int
    uid: int
    platform: str
    is_remake:bool
    title: str
    content: str
    author: str
    category: str
    reword: str
    link: str
    end_date: datetime.datetime
    created_at: int
    modified_at: int
