from dependency_injector import containers, providers

from .database import session_factory


class SqlAlchemyConatiner(containers.DeclarativeContainer):
    session = providers.Singleton(session_factory)
