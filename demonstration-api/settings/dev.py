import os

from sqlalchemy import engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from settings.database import DevDataBaseConnection

CORE = int(os.cpu_count())

db_engine = engine.create_engine(
    DevDataBaseConnection.get_url(),
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=5,
    pool_timeout=10,
    echo=True
)

db_session = scoped_session(sessionmaker(
    bind=db_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
))
