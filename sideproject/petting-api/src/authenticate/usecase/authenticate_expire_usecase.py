from __future__ import annotations

from dependency_injector.wiring import Provide

from adapter.kakao.api import KaKaoApi
from libs.abstract.abstract_usecase import AbstractUseCase as _AbstractUseCase
from settings.container.adapter_container import (
    KaKaoAdapterContainer as _KaKaoAdapterContainer
)
from src.session.entity import SessionEntity
from src.session.repository import SessionRDBRepository
from src.session.value_object import SessionChannel


class AuthenticateExpireUseCase(_AbstractUseCase):
    kakao_api: KaKaoApi = Provide[_KaKaoAdapterContainer.kako_api]

    def __init__(self):
        self.session_rdb_repository = SessionRDBRepository()

    def execute(self, session: SessionEntity):
        if session.channel == SessionChannel.KAKAO.value:
            self.kakao_api.user.logout(access_token=session.channel_code_to_json['access_token'])

        self.session_rdb_repository.delete_session_by_member_id(
            member_id=session.member_id
        )
