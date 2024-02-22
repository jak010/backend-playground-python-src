from __future__ import annotations

from abc import ABCMeta

from typing_extensions import Self


class AbstractEntity(metaclass=ABCMeta):
    id: int
    nanoid: str

    def __init__(self, *, id=None, nanoid=None, **kwargs):
        self.id = id
        self.nanoid = nanoid

        self.__dict__.update(kwargs)

    def __eq__(self, other: Self) -> bool:
        if isinstance(other, type(self)):
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
