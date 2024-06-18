from __future__ import annotations

import datetime
from enum import Enum

import nanoid

from libs.abstract.abstract_entity import AbstractEntity as _AbstractEntity


class CerificationType(Enum):
    SMS = 'SMS'


class CerificationStatus(Enum):
    REQUEST = 'REQUEST'
    COMPLETE = 'COMPLETE'


class CeritifcationEntity(_AbstractEntity):
    member_id: str
    phone: str
    type: str
    code: str
    status: str

    @classmethod
    def new(cls, member_id: str, phone: str, type: CerificationType, code: str, status: CerificationStatus) -> CeritifcationEntity:
        return cls(
            nanoid=nanoid.generate(size=24),
            member_id=member_id,
            phone=phone,
            type=type.value,
            code=code,
            status=status.value,
            created_at=datetime.datetime.now(),
            modified_at=datetime.datetime.now()
        )
