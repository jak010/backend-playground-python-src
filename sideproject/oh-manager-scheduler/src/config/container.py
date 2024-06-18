from dependency_injector import providers, containers

from adapter.database.session_factory import SQLALchemySessionFactory
from adapter.slack import Notification


class DataBaseContainer(containers.DeclarativeContainer):
    engine = providers.Dependency()

    session = providers.Singleton(SQLALchemySessionFactory.get_session, engine=engine)


class SlackContainer(containers.DeclarativeContainer):
    slack_token = providers.Dependency()
    slack_channel = providers.Dependency()

    notification = providers.Singleton(Notification, token=slack_token, channel=slack_channel)
