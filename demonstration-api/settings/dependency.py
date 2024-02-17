from dependency_injector import containers, providers

from settings.dev import get_session, get_engine


class DataBaseContainer(containers.DeclarativeContainer):

    _engine = providers.Factory(get_engine)

    session = providers.ThreadSafeSingleton(get_session, sa_engine=_engine.provider)
