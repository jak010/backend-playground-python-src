from dependency_injector import providers, containers

from adapter.database.client import DataBaseClient
from adapter.tmdb.api import TmdbAPI


class TmdbContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=['src']
    )

    tmdb_api_key = providers.Dependency()

    api = providers.Singleton(TmdbAPI, api_read_key=tmdb_api_key)


class DataBaseContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=['src']
    )

    db_url = providers.Dependency()

    db_client = providers.Singleton(
        DataBaseClient,
        db_url=db_url
    )
