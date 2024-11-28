from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session

from .settings import DataBaseSettings

print(DataBaseSettings.get_url_connection())
engine = create_engine(DataBaseSettings.get_url_connection(), echo=True)


def session_factory() -> Session:
    _session = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False
    )
    return scoped_session(_session)()
