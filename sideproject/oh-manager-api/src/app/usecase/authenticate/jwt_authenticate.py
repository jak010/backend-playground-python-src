import time

import jwt
from fastapi import HTTPException, Security, status

from src.app.domain.session import SessionEntity
from src.app.usecase.abstract import AbstractUseCase
from src.config.middleware import ApiKeyHeaderMiddleware
from src.libs import token_util


class JwtAuthenticate(AbstractUseCase):

    async def __call__(
            self,
            access_token=Security(ApiKeyHeaderMiddleware())
    ) -> SessionEntity:
        try:
            token_payload = token_util.verify_access_token(access_token=access_token)
        except jwt.exceptions.PyJWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        session = self.session_repository.get_by_session_id(session_id=token_payload['session_id'])
        if session is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if session.exp < int(time.time()):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return session
