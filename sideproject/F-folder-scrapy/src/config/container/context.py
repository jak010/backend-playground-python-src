from dependency_injector import containers, providers

from src.adapter.database.session.session_factory import SQLALchemySessionFactory


class ContextContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    engine = providers.Dependency()

    session = providers.Singleton(
        SQLALchemySessionFactory.get_session,
        engine=engine
    )
