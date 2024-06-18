from __future__ import annotations

from enum import Enum, unique


@unique
class PetPDTI(Enum):
    CLASS_CLOWN = 'CLASS_CLOWN'
    GUARDIAN = 'GUARDIAN'
    DEDICATED_WORKER = 'DEDICATED_WORKER'
    FAMILY_DOG = 'FAMILY_DOG'
    INDEPENDENT_THINKER = 'INDEPENDENT_THINKER'
    WATCH_DOG = 'WATCH_DOG'

    @classmethod
    def to(cls, value) -> PetPDTI:
        if value == 'CLASS_CLOWN':
            return PetPDTI.CLASS_CLOWN
        if value == 'GUARDIAN':
            return PetPDTI.GUARDIAN
        if value == 'DEDICATED_WORKER':
            return PetPDTI.DEDICATED_WORKER
        if value == 'FAMILY_DOG':
            return PetPDTI.FAMILY_DOG
        if value == 'INDEPENDENT_THINKER':
            return PetPDTI.INDEPENDENT_THINKER
        if value == 'WATCH_DOG':
            return PetPDTI.WATCH_DOG
        return None