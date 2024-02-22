from __future__ import annotations

from core.entity.abstract import AbstractEntity

import nanoid as _nanoid


class MemberEntity(AbstractEntity):
    name: str
    age: int

    @classmethod
    def new(cls, name: str, age: int):
        return cls(
            nanoid=_nanoid.generate(size=24),
            name=name,
            age=age
        )

    @classmethod
    def of(cls, id, nanoid, name, age):
        return cls(
            id=id,
            nanoid=nanoid,
            name=name,
            age=age
        )
