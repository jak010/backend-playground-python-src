import os

from sqlalchemy import engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.pool import QueuePool

from settings._database import DevDataBaseConnection, DevProxyDataBaseConnection
from typing import Callable

CORE = int(os.cpu_count())


def get_engine():
    return engine.create_engine(
        DevProxyDataBaseConnection.get_url(),
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=2,
        max_overflow=0,
        pool_timeout=60,
        echo=True
    )


def get_session(sa_engine):
    _session = scoped_session(
        sessionmaker(
            bind=sa_engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )
    )

    return _session


def get_db():
    _session = scoped_session(
        sessionmaker(
            bind=get_engine(),
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )
    )

    yield _session

    _session.commit()
    _session.close()


def patch_ioc():
    from settings.dependency import DataBaseContainer

    db = DataBaseContainer()

    db.wire(
        packages=['src']
    )
