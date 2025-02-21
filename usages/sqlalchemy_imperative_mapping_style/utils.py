from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import os
from sqlalchemy import engine
from sqlalchemy.orm import scoped_session

CORE = int(os.cpu_count())

DB_URL = URL.create(
    drivername="mysql+pymysql",
    username='root',
    password="1234",
    database="demo",
    host="127.0.0.1",
    port=19501
)

db_engine = engine.create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=5,
    pool_timeout=10,
    echo=True
)


def get_session():
    db_session: Session = scoped_session(sessionmaker(
        bind=db_engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    ))
    return db_session
