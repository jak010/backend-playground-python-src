import dataclasses
import time
import uuid
from enum import Enum
from typing import Optional, Union, List

from functools import cached_property

from src.app.domain.abstract import AbstractDomainEntity
from src.app.domain.member.command_query.member_category import MemberCategoryQuery, MemberCategoryMapper


class MemberActiveCode(Enum):
    DEACTIVE = 0
    ACTIVE = 1


@dataclasses.dataclass
class MemberEntity(AbstractDomainEntity):
    id: Optional[str] = dataclasses.field(default=None)
    email: str = dataclasses.field(default=None)
    password: str = dataclasses.field(default=None)
    is_active: MemberActiveCode = dataclasses.field(default=None)  # 0: 비활성화, 1: 활성화

    joined_at: int = dataclasses.field(default=None)
    created_at: int = dataclasses.field(default=None)
    modified_at: int = dataclasses.field(default=None)

    @classmethod
    def new(
            cls,
            email: str,
            password: str,
            is_active: MemberActiveCode
    ):
        return cls(
            id=str(uuid.uuid4()),
            email=email,
            password=password,
            is_active=is_active,
            joined_at=0,
            created_at=int(time.time()),
            modified_at=int(time.time())
        )

    @classmethod
    def by(
            cls,
            id: str,
            email: str,
            password: str,
            is_active: MemberActiveCode,
            joined_at: int,
            created_at: int,
            modified_at: int
    ):
        return cls(
            id=id,
            email=email,
            password=password,
            is_active=is_active,
            joined_at=joined_at,
            created_at=created_at,
            modified_at=modified_at,
        )

    def read(self, exclude_fields: list) -> dict:
        member_dict = dataclasses.asdict(self)
        for field in exclude_fields:
            member_dict.pop(field)

        return member_dict

    @cached_property
    def category(self) -> List[MemberCategoryMapper]:
        return MemberCategoryQuery.find_by(member_id=self.id)
