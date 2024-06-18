from __future__ import annotations

import dataclasses
import time

from src.app.domain.abstract import AbstractDomainEntity


@dataclasses.dataclass
class SessionEntity(AbstractDomainEntity):
    session_id: str = dataclasses.field(default=None)
    member_id: str = dataclasses.field(default=None)
    iat: int = dataclasses.field(default=None)
    exp: int = dataclasses.field(default=None)
    created_at: int = dataclasses.field(default=None)

    @classmethod
    def new(cls,
            *,
            id: int = None,
            session_id: str,
            member_id: str,
            iat: int,
            exp: int,
            ):
        return cls(
            id=id,
            session_id=session_id,
            member_id=member_id,
            iat=iat,
            exp=exp,
            created_at=int(time.time())
        )
