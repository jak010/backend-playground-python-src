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
                pool_size=4,
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
        # print(cls.__class__.__name__, cls.engine)

        session = sessionmaker(
            bind=cls.engine,
            autoflush=False,
            autocommit=False
        )
        session.configure(bind=cls.engine)

        return scoped_session(session)

# #
# if __name__ == '__main__':
#     localhost = "127.0.0.1"
#     port = 19501
#     username = "root"
#     password = "1234"
#
#     db_url = URL.create(
#         drivername="mysql+mysqldb",
#         username='root',
#         password="1234",
#         database="demo",
#         host="127.0.0.1",
#         port=19501
#     )

# Base Usage

# connection = SQLAlchemyConnector(db_url=db_url)
# session1 = connection.get_session()
# session2 = connection.get_session()
# print(session1)
# print(session2)
# print(session1 is session2)
# session1.remove()
# session2.remove()

# Test Usage

# Thread Test
# connection = SQLAlchemyConnector(db_url=db_url)

# def worker():
#     session = connection.get_session()
#     session.execute("select 1")
#     session.commit()
#     session.close()
#
#
# for _ in range(100_000):
#     th = threading.Thread(target=worker)
#     th.start()
