from __future__ import annotations

import json
from typing import TYPE_CHECKING

from src.member.entity import MemberEntity
from src.session.entity import SessionEntity
from src.session.repository import SessionRDBRepository
from src.session.value_object import SessionChannel

if TYPE_CHECKING:
    from adapter.kakao.api import KaKaoApi


class SessionService:
    session_rdb_repository = SessionRDBRepository()

    @classmethod
    def create_session_by_kakao(
            cls,
            member: MemberEntity,
            kakao_oauthenticatete,
            kakao_token
    ) -> SessionEntity:
        return SessionEntity.new(
            member_id=member.nanoid,
            channel=SessionChannel.KAKAO.value,
            channel_code=json.dumps({
                "type": kakao_oauthenticatete.token_type,
                "access_token": kakao_oauthenticatete.access_token,
                "refresh_token": kakao_oauthenticatete.refresh_token
            }),
            expire_time=kakao_token.expires_in_timestamp
        )

    def generate_session_from_kakao(
            self,
            session: SessionEntity,
            kakao_api: KaKaoApi
    ):
        """ KaKao Oauth 로그인에 의한 Session 생성
            - 한 사용자가 여러 Session을 사용하지 못함
        """
        if delete_sessions := self.session_rdb_repository.find_session_by_member_id(member_id=session.member_id):
            for delete_session in delete_sessions:
                if delete_session.channel == SessionChannel.KAKAO.value:
                    kakao_api.user.logout(access_token=delete_session.channel_code_to_json['access_token'])

        self.session_rdb_repository.delete_session_by_member_id(member_id=session.member_id)
        self.session_rdb_repository.add(session_entity=session)
