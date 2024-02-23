from __future__ import annotations

import nanoid as _nanoid

from core.entity.abstract import AbstractEntity
from core.entity.member_entity import MemberEntity


class MemberProfileEntity(AbstractEntity):
    description: str

    @classmethod
    def new(cls, descriptions):
        return cls(
            descriptions=descriptions
        )

    @classmethod
    def of(cls, id, nanoid, description):
        return cls(
            id=id,
            nanoid=nanoid,
            description=description
        )

    @classmethod
    def by(cls, member: MemberEntity, description):
        return cls(
            nanoid=member.nanoid,
            description=description
        )
