from __future__ import annotations

from src.domain.entity.abstract import AbstractEntity
from src.domain.entity.member_entity import MemberEntity


class MemberProfileEntity(AbstractEntity):
    description: str

    @classmethod
    def new(cls, nanoid, descriptions):
        return cls(
            nanoid=nanoid,
            descriptions=descriptions
        )

    @classmethod
    def of(cls, pk, nanoid, description):
        return cls(
            pk=pk,
            nanoid=nanoid,
            description=description
        )

    @classmethod
    def by(cls, member: MemberEntity, description):
        return cls(
            nanoid=member.nanoid,
            description=description
        )
