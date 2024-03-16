from __future__ import annotations

import dataclasses
import json
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

    @classmethod
    @abstractmethod
    def new(cls, *args, **kwargs):
        """ Entity 생성 시 구현 """
        raise NotImplementedError()

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
            if isinstance(value, AbstractValueObject):
                data[key] = value

        _formatter = f"{self.__class__.__name__}(" \
                     f"{data})"

        return _formatter


@dataclasses.dataclass(frozen=True)
class AbstractValueObject(metaclass=ABCMeta):

    def __str__(self):
        return f"{self.__class__.__name__}({json.dumps(dataclasses.asdict(self))})"

    def __ne__(self, other):
        return not self.__eq__(other)

    def __composite_values__(self): ...
