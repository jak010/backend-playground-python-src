import datetime
from typing import Optional, List

from pydantic import BaseModel
from src.pet.entity import PetEntity, PetAttachmentEntity
from src.pet.controller.dto import PetDto, PetAttachmentDto


class MemberInfoDTO(BaseModel):
    nanoid: str
    name: str
    email: str
    channel: str
    phone: str
    certificate_of_phone: bool
    certificate_of_phone_registered_at: Optional[datetime.datetime]
    terms_of_age: bool
    terms_of_agreement: bool
    terms_of_privacy: bool
    terms_of_geolocation: bool
    terms_of_marketing: bool
    created_at: datetime.datetime

    # pet
    pet: Optional[PetDto]
    pet_attachment: Optional[PetAttachmentDto]

    nickname: str
    birthday: datetime.datetime
    gender: str
    mbti: Optional[str]


class MemberTermsInfoDTO(BaseModel):
    nanoid: str
    name: str

    certificate_of_phone: bool
    certificate_of_phone_registered_at: Optional[datetime.datetime]
    terms_of_age: bool
    terms_of_agreement: bool
    terms_of_privacy: bool
    terms_of_geolocation: bool
    terms_of_marketing: bool
