from __future__ import annotations

from sqlalchemy.orm import sessionmaker, scoped_session


class SQLALchemySessionFactory:

    @classmethod
    def get_session(cls, engine):
        _Session = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            bind=engine,
        ))
        _Session.configure()

        return _Session
