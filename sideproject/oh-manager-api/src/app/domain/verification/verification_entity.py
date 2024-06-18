from __future__ import annotations

import dataclasses
import time
from enum import Enum

from src.app.domain.abstract import AbstractDomainEntity


class VerificationType(Enum):
    EMAIL = "EMAIL"


class VerificationStatus(Enum):
    PENDING = "PENDING"  # 인증 대기
    APPROVED = "APPROVED"  # 승인됨
    EXPIRED = "EXPIRED"  # 파기됨


@dataclasses.dataclass
class VerificationEntity(AbstractDomainEntity):
    sender: str = dataclasses.field(default=None)
    receiver: str = dataclasses.field(default=None)
    code: str = dataclasses.field(default=None)
    type: VerificationType = dataclasses.field(default=None)
    status: VerificationStatus = dataclasses.field(default=None)

    expired_at: int = dataclasses.field(default=None)
    created_at: int = dataclasses.field(default=None)
    modified_at: int = dataclasses.field(default=None)

    @classmethod
    def new(
            cls,
            sender: str,
            receiver: str,
            type: VerificationType,
            status: VerificationStatus,
            code: str
    ):
        return cls(
            sender=sender,
            receiver=receiver,
            type=type,
            code=code,
            status=status,
            expired_at=int(time.time()) + 1800,
            created_at=int(time.time()),
            modified_at=int(time.time())
        )
