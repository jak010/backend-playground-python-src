from abc import ABCMeta, abstractmethod
from typing import NoReturn

from notepad.structure.domain.model import MemberEntity


class IXXXRepository(metaclass=ABCMeta):

    @abstractmethod
    def find_by_id(self, *args, **kwrags) -> MemberEntity: ...

    @abstractmethod
    def save(self, *args, **kwrags) -> NoReturn: ...
