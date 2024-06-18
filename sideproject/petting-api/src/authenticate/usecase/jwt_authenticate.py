from __future__ import annotations

import time

import jwt
from fastapi import HTTPException, Security, status

from libs.abstract.abstract_usecase import AbstractUseCase as _AbstractUseCase
from libs.utils.token_utils import SessionToken
from settings.config.middleware import ApiKeyHeaderMiddleware
from src.session.entity.session_entity import SessionEntity
from src.session.repository import SessionRDBRepository


class JwtAuthenticate(_AbstractUseCase):
    session_repository = SessionRDBRepository()

    async def __call__(
            self,
            access_token=Security(ApiKeyHeaderMiddleware())
    ) -> SessionEntity:
        try:
            token_payload = SessionToken.decode_token(access_token=access_token)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        session = self.session_repository.find_session_by_nanoid(nanoid=token_payload.session_id)

        if session is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if session.expire_time < int(time.time()):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return session
