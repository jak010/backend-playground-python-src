from __future__ import annotations

import datetime

from libs.abstract.abstract_entity import AbstractEntity
from src.member.enums import MemberAssetType


class MemberAssetEntity(AbstractEntity):
    issued_quantity: int
    reason: str
    type: str

    created_at: datetime.datetime
    modified_at: datetime.datetime

    @classmethod
    def new(cls, member_id: str, issued_quantity: int, reason: str, type: MemberAssetType) -> MemberAssetEntity:
        return cls(
            nanoid=member_id,
            issued_quantity=issued_quantity,
            reason=reason,
            type=type.value,
            created_at=datetime.datetime.now(),
            modified_at=datetime.datetime.now()
        )

    def increase_quantity(self, quantity: int):
        self.issued_quantity = quantity
        self.modified_at = datetime.datetime.now()
