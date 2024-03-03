from __future__ import annotations
from abc import abstractmethod, ABCMeta, ABC
from typing import TypeVar, Generic, Type


class MyInterface(metaclass=ABCMeta):

    @abstractmethod
    def funciton(self):
        print(self)


T = TypeVar("T")


class AbsInterface(Generic[T]):
    session = "str"


# class ConcreateInterface(AbsInterface[MyInterface]):

