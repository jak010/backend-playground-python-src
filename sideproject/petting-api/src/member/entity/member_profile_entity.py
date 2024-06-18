from __future__ import annotations

import datetime
from typing import Optional

from libs.abstract.abstract_entity import AbstractEntity
from src.member.entity import MemberEntity
from src.member.enums import MemberMBTI, MemberGender


class MemberProfileEntity(AbstractEntity):
    nickname: str
    description: str

    address: str
    region1: str
    region2: str
    region3: str
    road_name: str

    latitude: float
    longitude: float

    job: str
    birthday: datetime.datetime
    gender: MemberGender
    mbti: MemberMBTI

    @classmethod
    def new(cls,
            member: MemberEntity,
            nickname: str,
            description: str,
            address: Optional[str],
            latitude: Optional[float],
            logitude: Optional[float],
            job: str,
            birthday: datetime.datetime,
            gender: MemberGender,
            mbti: Optional[MemberMBTI],
            ) -> MemberProfileEntity:
        return cls(
            nanoid=member.nanoid,
            nickname=nickname,
            description=description,
            address=address if address is not None else None,
            latitude=latitude if latitude is not None else None,
            logitude=logitude if logitude is not None else None,
            job=job,
            birthday=birthday,
            gender=gender.value,
            mbti=mbti.value if mbti is not None else None,
            created_at=datetime.datetime.now(),
            modified_at=datetime.datetime.now(),
        )
