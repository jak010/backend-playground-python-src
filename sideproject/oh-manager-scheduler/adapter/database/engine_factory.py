from __future__ import annotations

from abc import ABCMeta, abstractmethod

from sqlalchemy.engine import create_engine, URL


class AbstractEngineFactory(metaclass=ABCMeta):

    @abstractmethod
    def get_engine(self, *args, **kwargs): ...


class SQLALchemyEngineFactory(AbstractEngineFactory):

    @classmethod
    def get_engine(cls, url: URL):
        return create_engine(
            url,
            pool_pre_ping=True,
            pool_recycle=5,
            pool_size=5,
            pool_timeout=15,
            echo=True,
        )
