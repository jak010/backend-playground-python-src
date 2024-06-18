from __future__ import annotations

import dataclasses
import datetime
import time
from typing import Optional

from src.app.domain.abstract import AbstractDomainEntity


@dataclasses.dataclass
class ProfileEntity(AbstractDomainEntity):
    id: int = dataclasses.field(default=None)
    member_id: str = dataclasses.field(default=None)
    name: str = dataclasses.field(default=None)
    description: str = dataclasses.field(default=None)
    profile_url: Optional[str] = dataclasses.field(default=None)

    age: Optional[datetime.datetime] = dataclasses.field(default=None)
    gender: Optional[str] = dataclasses.field(default=None)

    body_weight: Optional[int] = dataclasses.field(default=None)
    body_height: Optional[int] = dataclasses.field(default=None)
    country: Optional[str] = dataclasses.field(default=None)
    address: Optional[str] = dataclasses.field(default=None)

    instargram_url: Optional[str] = dataclasses.field(default=None)
    facebook_url: Optional[str] = dataclasses.field(default=None)
    twitter_url: Optional[str] = dataclasses.field(default=None)
    profile_image: Optional[str] = dataclasses.field(default=None)

    created_at: int = dataclasses.field(default=None)
    modified_at: int = dataclasses.field(default=None)

    @classmethod
    def new(cls,
            member_id: Optional[str],
            name: str,
            description: str = None,
            profile_url: Optional[str] = None,
            age: Optional[datetime.datetime] = None,
            gender: Optional[str] = None,
            body_weight: Optional[int] = None,
            body_height: Optional[int] = None,
            country: Optional[str] = None,
            address: Optional[str] = None,
            instargram_url: Optional[str] = None,
            facebook_url: Optional[str] = None,
            twitter_url: Optional[str] = None,
            profile_image: Optional[str] = None
            ):
        return cls(
            member_id=member_id,
            name=name,
            description=description,
            profile_url=profile_url,
            age=age,
            gender=gender,
            body_weight=body_weight,
            body_height=body_height,
            country=country,
            address=address,
            instargram_url=instargram_url,
            facebook_url=facebook_url,
            twitter_url=twitter_url,
            profile_image=profile_image,
            created_at=int(time.time()),
            modified_at=int(time.time())
        )

    def update(
            self,
            member_id: Optional[str],
            name: str = None,
            description: str = None,
            profile_url: Optional[str] = None,
            age: Optional[datetime.datetime] = None,
            gender: Optional[str] = None,
            body_weight: Optional[int] = None,
            body_height: Optional[int] = None,
            country: Optional[str] = None,
            address: Optional[str] = None,
            instargram_url: Optional[str] = None,
            facebook_url: Optional[str] = None,
            twitter_url: Optional[str] = None,
            profile_image: Optional[str] = None
    ):
        self.member_id = member_id
        self.name = name if name is not None else self.name
        self.description = description if description is not None else self.description
        self.profile_url = profile_url if profile_url is not None else self.profile_url
        self.age = age if age is not None else self.age
        self.gender = gender if gender is not None else self.gender
        self.body_weight = body_weight if body_weight is not None else self.body_weight
        self.body_height = body_height if body_height is not None else self.body_height
        self.country = country if country is not None else self.country
        self.address = address if address is not None else self.address
        self.instargram_url = instargram_url if instargram_url is not None else self.instargram_url
        self.facebook_url = facebook_url if facebook_url is not None else self.facebook_url
        self.twitter_url = twitter_url if twitter_url is not None else self.twitter_url
        self.profile_image = profile_image if profile_image is not None else self.profile_image
        self.modified_at = int(time.time())
        return self

    def read(self, exclude_fields: list) -> dict:
        profile_dict = dataclasses.asdict(self)
        for field in exclude_fields:
            profile_dict.pop(field)
        return profile_dict
