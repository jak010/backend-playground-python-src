from __future__ import annotations

from abc import ABCMeta, abstractmethod

from sqlalchemy.orm import sessionmaker, scoped_session


class AbstractSessionFactory(metaclass=ABCMeta):

    @abstractmethod
    def get_session(self, *args, **kwargs): ...


class SQLALchemySessionFactory(AbstractSessionFactory):

    @classmethod
    def get_session(cls, engine):
        session_local = scoped_session(sessionmaker(
            bind=engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        ))

        return session_local()
