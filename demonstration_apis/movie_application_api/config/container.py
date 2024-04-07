import os

from dependency_injector import providers, containers

from adapter.tmdb.api import TmdbAPI


class TmdbContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=['src']
    )

    tmdb_api_key = providers.Dependency()

    api = providers.Singleton(TmdbAPI, api_read_key=tmdb_api_key)
