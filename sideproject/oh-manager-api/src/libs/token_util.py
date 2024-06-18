from __future__ import annotations

import jwt

from src.config.settings import constant


def create_access_token(
        session_id: str,
        member_id: str,
        iat: int,
        exp: int
) -> str:
    return jwt.encode(
        payload={
            "session_id": str(session_id),
            "member_id": str(member_id),
            "iat": iat,
            "exp": exp
        },
        key=constant.SECRET_KEY,
        algorithm='HS256'
    )


def verify_access_token(access_token: str):
    try:
        return jwt.decode(
            jwt=access_token,
            key=constant.SECRET_KEY,
            algorithms='HS256'
        )
    except jwt.exceptions.PyJWTError as e:
        raise e
