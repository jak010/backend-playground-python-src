from __future__ import annotations

import datetime
from typing import Optional

from libs.abstract.abstract_entity import AbstractEntity
from src.member.enums import MemberSIGNUPChannel, MemberOnboardStatus


class MemberEntity(AbstractEntity):
    name: str
    email: str
    password: str
    channel: str
    is_onboard: int
    phone: str
    coin: int

    certificate_of_phone: bool
    certificate_of_phone_registered_at: Optional[datetime.datetime]

    terms_of_age: bool
    terms_of_agreement: bool
    terms_of_privacy: bool
    terms_of_geolocation: bool
    terms_of_marketing: bool

    @classmethod
    def new(cls,
            *,
            name: str,
            email: str,
            channel: MemberSIGNUPChannel,
            phone: str,
            terms_of_marketing: bool
            ) -> MemberEntity:
        return cls(
            nanoid=cls.generate_nano_id(),
            name=name,
            email=email,
            channel=channel.value,
            phone=phone,
            coin=0,

            certificate_of_phone=False,
            certificate_of_phone_registered_at=None,

            terms_of_age=True,
            terms_of_agreement=True,
            terms_of_privacy=True,
            terms_of_geolocation=True,
            terms_of_marketing=terms_of_marketing,

            created_at=datetime.datetime.now(),
            modified_at=datetime.datetime.now(),
        )

    @classmethod
    def of_kakao(cls, *, name: str, email: str, phone: str) -> MemberEntity:
        """ KaKao 가입에 의한 Entity 생성 """
        return cls(
            nanoid=cls.generate_nano_id(),
            name=name,
            email=email,
            channel=MemberSIGNUPChannel.KAKAO.KAKAO.value,

            phone=phone,

            certificate_of_phone=False,
            certificate_of_phone_registered_at=None,

            terms_of_age=False,
            terms_of_agreement=False,
            terms_of_privacy=False,
            terms_of_geolocation=False,
            terms_of_marketing=False,

            created_at=datetime.datetime.now(),
            modified_at=datetime.datetime.now(),
        )

    def increase_coin(self, quantity):
        self.coin = self.coin + quantity
        self.modified_at = datetime.datetime.now()

    def onboard_complete(self):
        self.is_onboard = MemberOnboardStatus.TRUE.value
        self.modified_at = datetime.datetime.now()

    @property
    def phone_number(self):
        national_code, phone_number = self.phone.split(" ")
        if national_code == "+82":
            return "0" + phone_number
