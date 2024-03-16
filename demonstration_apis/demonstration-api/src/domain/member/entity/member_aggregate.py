from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar, List

from src.domain.abstract import AbstractEntity
from src.domain.member.entity import MemberEntity, MemberProfileEntity

ROOT_ENTITY = TypeVar("ROOT_ENTITY", bound=AbstractEntity)


class AbstarctAggregate(Generic[ROOT_ENTITY]):
    root_entity_id: ROOT_ENTITY.nanoid

    @classmethod
    @abstractmethod
    def new(cls, root_entity: ROOT_ENTITY, **kwargs): ...

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class MemberAggregate(AbstarctAggregate[MemberEntity]):
    root_entity: MemberEntity
    profile: List[MemberProfileEntity]

    @classmethod
    def new(
            cls,
            root_entity: ROOT_ENTITY,
            profile: MemberProfileEntity = None
    ):
        return cls(
            root_entity=root_entity,
            profile=profile
        )
