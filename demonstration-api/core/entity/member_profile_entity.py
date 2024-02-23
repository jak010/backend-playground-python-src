from __future__ import annotations

import nanoid as _nanoid

from core.entity.abstract import AbstractEntity
from core.entity.member_entity import MemberEntity


class MemberProfileEntity(AbstractEntity):
    member_id: str
    description: str

    @classmethod
    def new(cls, member_id, descriptions):
        return cls(
            member_id=member_id,
            descriptions=descriptions
        )

    @classmethod
    def of(cls, pk, member_id, description):
        return cls(
            pk=pk,
            member_id=member_id,
            description=description
        )

    @classmethod
    def by(cls, member: MemberEntity, description):
        return cls(
            member_id=member.member_id,
            description=description
        )
