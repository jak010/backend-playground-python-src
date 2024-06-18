from __future__ import annotations

from enum import unique, Enum


@unique
class PetAttachmentType(Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"

    @classmethod
    def to(cls, value: str) -> PetAttachmentType:
        if value == cls.PRIMARY.value:
            return PetAttachmentType.PRIMARY
        if value == cls.SECONDARY.value:
            return PetAttachmentType.SECONDARY


@unique
class PetAttachmentLabel(Enum):
    PET = "PET"
    SELFIE = "SELFIE"

    @classmethod
    def to(cls, value: str) -> PetAttachmentLabel:
        if value == cls.PET.value:
            return PetAttachmentLabel.PET
        if value == cls.SELFIE.value:
            return PetAttachmentLabel.SELFIE
