from __future__ import annotations

from src.member.entity import MemberEntity
from src.member.enums import MemberSIGNUPChannel


class MemberService:

    @staticmethod
    def create_member(name: str, email: str, phone: str, channel: MemberSIGNUPChannel, terms_of_marketing: bool) -> MemberEntity:
        return MemberEntity.new(
            name=name,
            email=email,
            phone=phone,
            channel=channel,
            terms_of_marketing=terms_of_marketing
        )

    @staticmethod
    def new_member_with_kakao(name: str, email: str, phone: str) -> MemberEntity:
        return MemberEntity.of_kakao(
            name=name,
            email=email,
            phone=phone
        )
