from __future__ import annotations

from abc import ABCMeta, abstractmethod

import nanoid as _nanoid
from typing_extensions import Self


def generate_entity_id():
    return _nanoid.generate(size=24)


class AbstractEntity(metaclass=ABCMeta):
    # Definition Attribute
    pk: int
    nanoid: str

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def __eq__(self, other: Self) -> bool:
        if isinstance(self, type(other)):
            return self.nanoid == other.nanoid
        return False

    def __hash__(self):
        return hash(self.nanoid)

    def __str__(self):
        data = {}

        for key, value in self.__dict__.items():
            if '_' not in key:
                data[key] = str(value)

        _formatter = f"{self.__class__.__name__}(" \
                     f"{data})"

        return _formatter


class MemberEntity(AbstractEntity):
    profie: MemberProfileEntity


class MemberProfileEntity(AbstractEntity):
    description: str
