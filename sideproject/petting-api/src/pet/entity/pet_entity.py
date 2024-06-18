from __future__ import annotations

import datetime

from libs.abstract.abstract_entity import AbstractEntity
from src.pet.enums import (
    PetPDTI,
    PetPDTIType,
    PetNeuteredStatus
)


class PetEntity(AbstractEntity):
    owner: str
    name: str
    gender: str
    neutered_status: bool
    breed: str
    pdti: str
    pdti_type: str

    @classmethod
    def new(cls,
            owner: str,
            name: str,
            gender: str,
            neutered_status: PetNeuteredStatus,
            breed: str,
            pdti: PetPDTI = None,
            pdti_type: PetPDTIType = None
            ) -> PetEntity:
        return cls(
            nanoid=cls.generate_nano_id(),
            owner=owner,
            name=name,
            gender=gender,
            neutered_status=neutered_status.value if neutered_status else None,
            breed=breed,
            pdti=pdti.value if pdti_type else None,
            pdti_type=pdti_type.value if pdti_type else None,
            created_at=datetime.datetime.now(),
            modified_at=datetime.datetime.now()
        )
