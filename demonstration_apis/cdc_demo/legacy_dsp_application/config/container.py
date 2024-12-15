from dependency_injector import containers, providers

from .database import session_factory


class SqlAlchemyConatiner(containers.DeclarativeContainer):
    session = providers.Factory(session_factory)


class EventContainer(containers.DeclarativeContainer):
    event_store = providers.Singleton(list)
