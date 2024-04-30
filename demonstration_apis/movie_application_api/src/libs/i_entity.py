from __future__ import annotations

from abc import ABCMeta


class AbstractEntity(metaclass=ABCMeta):
    pk: int

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def eq(self, other: AbstractEntity) -> bool:
        return self.pk == other.pk
