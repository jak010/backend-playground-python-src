from __future__ import annotations

import dataclasses
import datetime
import time
from enum import Enum

from src.app.domain.abstract import AbstractDomainEntity


class AuditionCategory(Enum):
    MOVIE = "영화"


@dataclasses.dataclass
class AuditionEntity(AbstractDomainEntity):
    uid: str = dataclasses.field(default=None)
    platform: str = dataclasses.field(default=None)
    is_remake: str = dataclasses.field(default=None)
    title: str = dataclasses.field(default=None)
    content: str = dataclasses.field(default=None)
    category: AuditionCategory = dataclasses.field(default=None)
    author: str = dataclasses.field(default=None)
    reward: str = dataclasses.field(default=None)
    link: str = dataclasses.field(default=None)
    end_date: datetime.datetime = dataclasses.field(default=None)
    created_at: int = dataclasses.field(default=None)
    modified_at: int = dataclasses.field(default=None)

    @classmethod
    def new(cls,
            uid: str = None,
            platform: str = None,
            is_remake: bool = None,
            title: str = None,
            content: str = None,
            category: str = None,
            author: str = None,
            reward: str = None,
            link: str = None,
            end_date: datetime.datetime = None
            ) -> AuditionEntity:
        return cls(
            uid=uid,
            platform=platform,
            is_remake=is_remake,
            title=title,
            content=content,
            category=category,
            author=author,
            reward=reward,
            link=link,
            end_date=end_date,
            created_at=int(time.time()),
            modified_at=int(time.time())
        )

    def read(self, exclude_fields: list):
        data = self.to_dict()
        for field in exclude_fields:
            data.pop(field)
        return data
