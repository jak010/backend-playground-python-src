from __future__ import annotations

from sqlalchemy.engine import create_engine, URL
from sqlalchemy.orm import sessionmaker, scoped_session


class DataBaseClient:
    """Acts as a connection pool and session factory."""

    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(
            self.db_url,
            pool_pre_ping=True,
            pool_recycle=5,
            pool_size=5,
            pool_timeout=15,
            echo=True,
        )
        self.session_factory = scoped_session(sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        ))

    def session(self):
        return self.session_factory()
