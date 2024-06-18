from __future__ import annotations

from dependency_injector.wiring import Provide

from adapter.kakao.api import KaKaoApi
from libs.abstract.abstract_usecase import AbstractUseCase as _AbstractUseCase
from libs.utils.token_utils import SessionToken
from settings.container.adapter_container import (
    KaKaoAdapterContainer as _KaKaoAdapterContainer
)
from src.member.repository import (
    MemberRDBRepository, MemberProfileRDBRepository
)
from src.member.service import (
    MemberService, MemberProfileService
)
from src.session.repository import SessionRDBRepository
from src.session.service import SessionService


class KaKaoAuthenticateFailureException(Exception):
    """ KaKao 로그인 실패 """


class KaKoaUseCase(_AbstractUseCase):
    kakao_api: KaKaoApi = Provide[_KaKaoAdapterContainer.kako_api]

    def __init__(self):
        self.member_repository = MemberRDBRepository()
        self.member_profile_repository = MemberProfileRDBRepository()
        self.session_repository = SessionRDBRepository()
        self.session_service = SessionService()


class KaKaoOauthAuthorizedCodeUseCase(KaKoaUseCase):
    """ KaKao Oauth, Authorization code 요청 """

    def execute(self) -> str:
        return self.kakao_api.oauth.get_authorization_url()


class KaKaoAuthenticateUseCase(KaKoaUseCase):

    def execute(self, authorization_code: str) -> SessionToken:
        """ KaKao Oauth, Access Token 발급 """
        try:
            kakao_oauthenticatete = self.kakao_api.oauth.get_access_token(authorization_code=authorization_code)
            kakao_user = self.kakao_api.user.info(access_token=kakao_oauthenticatete.access_token)
            kakao_token = self.kakao_api.token.get_access_token_info(access_token=kakao_oauthenticatete.access_token)
        except Exception as e:
            raise KaKaoAuthenticateFailureException from e

        member = self.member_repository.find_member_by_email(email=kakao_user.kakao_account['email'])
        if member:
            session = self.session_service.create_session_by_kakao(
                member=member,
                kakao_oauthenticatete=kakao_oauthenticatete,
                kakao_token=kakao_token
            )
            self.session_service.generate_session_from_kakao(session=session, kakao_api=self.kakao_api)

            return self._create_session_token_v1(kakao_token, member, session)
        else:
            return self._register_member_after_create_session_token(
                kakao_token=kakao_token,
                kakao_oauthenticatete=kakao_oauthenticatete,
                kakao_user=kakao_user
            )

    def _register_member_after_create_session_token(self, kakao_token, kakao_oauthenticatete, kakao_user):
        """ KaKao Oauth 시, DB에 Member가 등록되어 있지 않다면 등록하고 SessionToken 생성 """
        member = MemberService.new_member_with_kakao(
            name=kakao_user.kakao_account['profile']['nickname'],
            email=kakao_user.kakao_account['email'],
            phone=kakao_user.kakao_account['phone_number']
        )
        member_profile = MemberProfileService.from_kakao(
            member=member,
            kakao_user=kakao_user
        )
        session = self.session_service.create_session_by_kakao(
            member=member,
            kakao_oauthenticatete=kakao_oauthenticatete,
            kakao_token=kakao_token
        )

        self.member_repository.add(member_entity=member)
        self.member_profile_repository.add(member_profile_entity=member_profile)
        self.session_service.generate_session_from_kakao(session=session, kakao_api=self.kakao_api)

        return self._create_session_token_v1(kakao_token, member, session)

    def _create_session_token_v1(self, kakao_token, member, session) -> SessionToken:
        return SessionToken.new(
            session_id=session.nanoid,
            member_id=member.nanoid,
            email=member.email,
            channel=member.channel,
            issued_time=session.issued_time,
            expired_time=kakao_token.expires_in_timestamp
        )
