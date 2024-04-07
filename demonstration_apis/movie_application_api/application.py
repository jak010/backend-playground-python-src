from fastapi import FastAPI

from src.controller import controller_router

from config.settings import LocalSetting
from config.container import TmdbContainer
from config.constants import TMDBConfig


class MoveAppsApplication:
    settings = LocalSetting()

    def __call__(self, *args, **kwargs):
        self.settings.application(
            app=FastAPI(
                title="MOIVE APPS"
            )
        )
        self.settings.adapter_patch(
            containers=[
                TmdbContainer(tmdb_api_key=TMDBConfig.TMDB_API_READ_KEY.value)
            ]
        )
        self.settings.include_routers(
            routers=[
                controller_router
            ]
        )

        return self.settings.app


application = MoveAppsApplication()
