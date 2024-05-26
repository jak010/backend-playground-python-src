from typing import Generic, TypeVar
from fastapi import Depends
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from functools import cache
from external_library.database import SQLAlchemyConnector

M = TypeVar("M", bound=declarative_base())


class AbstractRdbRepsitory(Generic[M]):
    session: Session

    @classmethod
    def get_session(cls):
        return cls.session

    def find_by_id(self, *args, **kwargs) -> M: ...
