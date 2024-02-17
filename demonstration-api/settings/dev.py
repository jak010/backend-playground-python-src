import os

from sqlalchemy import engine
from sqlalchemy.orm import scoped_session, sessionmaker

from settings._database import DevDataBaseConnection
from typing import Callable

CORE = int(os.cpu_count())


def get_engine() -> Callable:
    return engine.create_engine(
        DevDataBaseConnection.get_url(),
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=5,
        max_overflow=5,
        pool_timeout=10,
        echo=True
    )


def get_session(sa_engine):
    _session = scoped_session(sessionmaker(
        bind=sa_engine(),
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    ))

    return _session


def get_db():
    db = get_session(get_engine())
    try:
        yield db
    finally:
        db.close()


def patch_ioc():
    from settings.dependency import DataBaseContainer

    db = DataBaseContainer()
    db.wire(
        packages=['src']
    )
    return db
