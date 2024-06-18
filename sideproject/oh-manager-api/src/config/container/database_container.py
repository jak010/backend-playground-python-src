from dependency_injector import providers, containers


class DataBaseContainer(containers.DeclarativeContainer):
    from adapter.database.session_factory import SQLALchemySessionFactory

    engine = providers.Dependency()

    session = providers.Singleton(SQLALchemySessionFactory.get_session, engine=engine)
