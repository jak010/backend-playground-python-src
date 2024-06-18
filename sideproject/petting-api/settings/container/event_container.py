from dependency_injector import providers, containers
from sqlalchemy.orm.session import Session

from adapter.database.connector import SQLALchemyConnector
from libs.abstract.event_dispatcher import EventHandler


class EventContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=['src']
    )

    handler = providers.Singleton(EventHandler)
