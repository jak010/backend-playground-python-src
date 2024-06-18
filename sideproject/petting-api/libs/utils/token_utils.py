from __future__ import annotations

import dataclasses

import jwt

from settings.config.base import TOKEN_SCRET as _TOKEN_SCRET


@dataclasses.dataclass
class SessionToken:
    session_id: str
    member_id: str
    email: str
    channel: str

    issued_time: int
    expired_time: int

    @classmethod
    def new(cls,
            session_id: str,
            member_id: str,
            email: str,
            channel: str,

            issued_time: int,
            expired_time: int
            ):
        return cls(
            session_id=session_id,
            member_id=member_id,
            email=email,
            channel=channel,

            issued_time=issued_time,
            expired_time=expired_time
        )

    def generate_token(self):
        return jwt.encode(
            {
                "session_id": self.session_id,
                "member_id": self.member_id,
                "email": self.email,
                "channel": self.channel,

                "issued_time": self.issued_time,
                "expired_time": self.expired_time
            },
            _TOKEN_SCRET,
            algorithm="HS256"
        )

    @classmethod
    def decode_token(cls, access_token: str) -> SessionToken:
        try:
            data = jwt.decode(access_token, _TOKEN_SCRET, algorithms='HS256')
            return cls(**data)
        except Exception as e:
            raise Exception("Token Decode Error", e)
