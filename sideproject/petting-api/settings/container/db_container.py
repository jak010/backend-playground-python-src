from dependency_injector import providers, containers
from sqlalchemy.orm.session import Session

from adapter.database.connector import SQLALchemyConnector


class DataBaseContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=['src']
    )

    db_url = providers.Dependency()

    engine = providers.Singleton(
        SQLALchemyConnector.get_engine,
        db_url
    )

    session: Session = providers.Singleton(
        SQLALchemyConnector.get_session,
        engine=engine
    )
