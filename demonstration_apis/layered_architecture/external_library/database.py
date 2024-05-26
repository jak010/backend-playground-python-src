from __future__ import annotations
import contextlib

from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.engine import create_engine
import threading
from functools import cached_property, cache, lru_cache
from typing import Generator
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base


class SQLAlchemyConnector:
    url: str
    engine: Engine = None

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.engine = kwargs.get("engine")
        return obj

    @classmethod
    def with_url(cls, url: str):
        object = cls(
            engine=create_engine(
                url,
                pool_size=3,
                max_overflow=1,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=True
            ))
        cls.engine = object.engine

        return object

    @classmethod
    def get_engine(cls):
        return cls.engine

    @classmethod
    def get_session(cls):
        session = sessionmaker(
            bind=cls.engine,
            autoflush=False,
            autocommit=False
        )

        return scoped_session(session)
