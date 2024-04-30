from fastapi import FastAPI

from config.configuration import TMDBConfiguration, DataBaseConfiguration
from config.container import TmdbContainer, DataBaseContainer
from config.settings import LocalSetting
from src.member.controller import member_router


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
                DataBaseContainer(db_url=DataBaseConfiguration.get_db_url()),
                TmdbContainer(tmdb_api_key=TMDBConfiguration.TMDB_API_READ_KEY.value),
            ]
        )
        self.settings.include_routers(
            routers=[
                member_router
            ]
        )

        return self.settings.app


application = MoveAppsApplication()
