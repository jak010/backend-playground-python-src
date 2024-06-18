from __future__ import annotations

import dataclasses
import datetime
from typing import TypedDict


class KaKaoProfile(TypedDict):
    nickname: str
    thumbnail_image_url: str
    profile_image_url: str
    is_default_image: bool


class KaKaoUserAccount(TypedDict):
    profile_nickname_needs_agreement: bool
    profile_image_needs_agreement: bool
    profile: KaKaoProfile
    name_needs_agreement: bool
    name: str
    has_email: bool
    email_needs_agreement: bool
    is_email_valid: bool
    is_email_verified: bool
    email: str
    has_phone_number: bool
    phone_number_needs_agreement: bool
    phone_number: str
    has_age_range: bool
    age_range_needs_agreement: bool
    age_range: str
    has_birthyear: bool
    birthyear_needs_agreement: bool
    birthyear: str
    has_birthday: bool
    birthday_needs_agreement: bool
    birthday: str
    birthday_type: str
    has_gender: bool
    gender_needs_agreement: bool
    gender: str


class KaKaoUserInfoProperties(TypedDict):
    nickname: str
    profile_image: str
    thumbnail_image: str


@dataclasses.dataclass(frozen=True)
class KaKaoUserInfoDto:
    id: int
    connected_at: datetime.datetime
    properties: KaKaoUserInfoProperties  # nickname, profile_image, thumbnail_image
    kakao_account: KaKaoUserAccount  # profile_nickname_needs_agreement, profile_image_needs_agreement, profile:dict

    """
    {
        "id"          : ,
        "connected_at": "",
        "properties": {
            "nickname"       : "",
            "profile_image"  : "",
            "thumbnail_image": ""
        },
        "kakao_account": {
            "profile_nickname_needs_agreement": false,
            "profile_image_needs_agreement"   : false,
            "profile":{
                "nickname"                    : "",
                "thumbnail_image_url"         : "",
                "profile_image_url"           : ",
                "is_default_image"            : false
            },
            "name_needs_agreement"            : false,
            "name"                            : "",
            "has_email"                       : true,
            "email_needs_agreement"           : false,
            "is_email_valid"                  : true,
            "is_email_verified"               : true,
            "email"                           : "",
            "has_phone_number"                : true,
            "phone_number_needs_agreement"    : false,
            "phone_number"                    : "+82 10-1234-1234",
            "has_age_range"                   : true,
            "age_range_needs_agreement"       : false,
            "age_range"                       : "11~11",
            "has_birthyear"                   : true,
            "birthyear_needs_agreement"       : false,
            "birthyear"                       : "1995",
            "has_birthday"                    : true,
            "birthday_needs_agreement"        : false,
            "birthday"                        : "1225",
            "birthday_type"                   : "SOLAR",
            "has_gender"                      : true,
            "gender_needs_agreement"          : false,
            "gender"                          : "male"
        }
    }
    """
