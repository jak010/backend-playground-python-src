from typing import Generic, TypeVar, ParamSpec, Optional
from abc import abstractmethod
from core.domain.entity import MemberEntity, MemberProfileEntity
from core.domain.entity.abstract import AbstractEntity

ROOT_ENTITY = TypeVar("ROOT_ENTITY", bound=AbstractEntity)

import dataclasses


@dataclasses.dataclass
class AbstarctAggregate(Generic[ROOT_ENTITY]):

    @classmethod
    @abstractmethod
    def new(cls, entity: ROOT_ENTITY, **kwargs): ...


@dataclasses.dataclass
class MemberAggregate(AbstarctAggregate[MemberEntity]):
    member: ROOT_ENTITY
    member_profile: MemberProfileEntity

    @classmethod
    def new(
            cls,
            root_entitiy: ROOT_ENTITY,
            member_profile: MemberProfileEntity = None
    ):
        return cls(
            member=root_entitiy,
            member_profile=member_profile
        )

    def exist_member_profile(self):
        if self.member_profile is not None:
            return self.member_profile
        raise Exception("Member Profile Not Exist")
