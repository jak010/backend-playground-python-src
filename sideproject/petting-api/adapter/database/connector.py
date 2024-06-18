from __future__ import annotations

from abc import ABCMeta, abstractmethod

from sqlalchemy.engine import create_engine, URL
from sqlalchemy.orm import sessionmaker, scoped_session


class SQLAlchemyConnectorInterface(metaclass=ABCMeta):

    @abstractmethod
    def get_engine(self, *args, **kwargs): ...

    @abstractmethod
    def get_session(self, *args, **kwargs): ...


class SQLALchemyConnector(SQLAlchemyConnectorInterface):

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

    @classmethod
    def get_session(cls, engine):
        session_local = scoped_session(sessionmaker(
            bind=engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        ))

        return session_local()
