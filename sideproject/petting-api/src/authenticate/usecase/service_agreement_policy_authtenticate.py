from __future__ import annotations

import time

import jwt
from fastapi import HTTPException, Security, status

from libs.abstract.abstract_usecase import AbstractUseCase as _AbstractUseCase
from libs.utils.token_utils import SessionToken
from settings.config.middleware import ApiKeyHeaderMiddleware
from src.member.repository import MemberRDBRepository
from src.session.repository import SessionRDBRepository

from src.session.entity import SessionEntity


class ServiceAgreementPolicyAuthenticate(_AbstractUseCase):
    session_repository = SessionRDBRepository()
    member_rdb_repository = MemberRDBRepository()

    async def __call__(
            self,
            access_token=Security(ApiKeyHeaderMiddleware())
    ) -> SessionEntity:

        try:
            token_payload = SessionToken.decode_token(access_token=access_token)
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        session = self.session_repository.find_session_by_nanoid(nanoid=token_payload.session_id)

        if session is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if session.member is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if session.expire_time < int(time.time()):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if not all([
            session.member.terms_of_agreement,
            session.member.terms_of_geolocation,
            session.member.terms_of_age,
            session.member.terms_of_privacy
        ]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This user cannot access the service as they have not agreed to the terms of service."
            )

        return session
