import datetime
from abc import ABCMeta, abstractmethod

from .aggregate_type import AggregatedType


class DomainEvent(metaclass=ABCMeta):

    @abstractmethod
    def aggregate_type(self) -> AggregatedType:
        """ 해당 도메인의 타입 """
        ...

    @abstractmethod
    def aggregate_id(self) -> int:
        """ 도메인의 식별자 """
        ...

    @abstractmethod
    def occured_on(self) -> datetime.datetime:
        """ 이벤트가 발생한 시간 """
        ...

    @abstractmethod
    def ower_id(self) -> int:
        """ 도메인이 누구에게 속하는가 """
        ...
