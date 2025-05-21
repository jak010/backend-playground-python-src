import os

from sqlalchemy import engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker, Session

CORE = int(os.cpu_count())

DB_URL = URL.create(
    drivername="mysql+pymysql",
    username='root',
    password="1234",
    database="demo",
    host="127.0.0.1",
    port=19501
)


def get_engine() -> engine.Engine:
    return engine.create_engine(
        DB_URL,
        pool_pre_ping=False,
        pool_recycle=3600,
        pool_size=50,
        max_overflow=100,
        pool_timeout=10,
        echo=False
    )


def get_session(engine) -> Session:
    db_session = scoped_session(sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    ))
    return db_session
