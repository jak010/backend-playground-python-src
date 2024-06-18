from __future__ import annotations

from enum import Enum, unique


@unique
class PetPDTIType(Enum):
    T = 'T'
    F = 'F'

    @classmethod
    def to(cls, value) -> PetPDTIType:
        if value == 'T':
            return PetPDTIType.T
        if value == 'F':
            return PetPDTIType.F
        return None
