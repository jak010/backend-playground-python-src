from __future__ import annotations

from enum import Enum, unique


@unique
class PetNeuteredStatus(Enum):
    T = 'T'
    F = 'F'

    @classmethod
    def to(cls, value: str) -> PetNeuteredStatus:
        if value == cls.T.value:
            return PetNeuteredStatus.T
        if value == cls.F.value:
            return PetNeuteredStatus.F
        return None
