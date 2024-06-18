from __future__ import annotations

from adapter.kakao.resource.user.dto.kakao_user_info_dto import KaKaoUserInfoDto
from libs.utils import time_utils
from src.member.entity import (
    MemberEntity,
    MemberProfileEntity
)
from src.member.enums import MemberGender


class MemberProfileService:

    @staticmethod
    def from_kakao(
            member: MemberEntity,
            kakao_user: KaKaoUserInfoDto
    ) -> MemberProfileEntity:
        return MemberProfileEntity.new(
            member=member,
            nickname=kakao_user.kakao_account['name'],

            description="",
            address=None,
            latitude=None,
            logitude=None,
            job="",
            birthday=time_utils.parse_birthday(
                birthyear=kakao_user.kakao_account['birthyear'],
                birthday=kakao_user.kakao_account['birthday']
            ),
            gender=MemberGender.to_obj(gender=kakao_user.kakao_account['gender'].upper()),
            mbti=None
        )
