from __future__ import annotations

import dataclasses
import time

from src.app.domain.abstract import AbstractDomainEntity


@dataclasses.dataclass
class SubmissionEntity(AbstractDomainEntity):
    audition_id: str = dataclasses.field(default=None)
    member_id: str = dataclasses.field(default=None)
    status: str = dataclasses.field(default=None) # TODO 24.01.28 : SUBMISSION 상태 체크 필요
    created_at: int = dataclasses.field(default=None)
    modified_at: int = dataclasses.field(default=None)

    @classmethod
    def new(cls,
            audition_id: str = None,
            member_id: str = None,
            status: str = None
            ):
        return cls(
            audition_id=audition_id,
            member_id=member_id,
            status=status,
            created_at=int(time.time()),
            modified_at=int(time.time())
        )
