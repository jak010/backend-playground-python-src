from __future__ import annotations

from abc import ABCMeta, abstractmethod

from typing_extensions import Self


class AbstractEntity(metaclass=ABCMeta):
    id: int
    nanoid: str

    def __init__(self, *, id=None, nanoid=None, **kwargs):
        self.id = id
        self.nanoid = nanoid

        self.__dict__.update(kwargs)

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

        _formatter = f"{self.__class__.__name__}(" \
                     f"{data})"

        return _formatter
