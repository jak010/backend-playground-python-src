from dependency_injector import containers, providers

from settings.dev import get_session, get_engine, get_db


class DataBaseContainer(containers.DeclarativeContainer):
    _engine = providers.Singleton(get_engine)

    session = providers.Singleton(get_session, sa_engine=_engine.provided)
    resource_session = providers.Resource(get_db)
