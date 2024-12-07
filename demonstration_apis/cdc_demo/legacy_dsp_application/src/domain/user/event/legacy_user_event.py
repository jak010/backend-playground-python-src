from __future__ import annotations

import datetime
from abc import abstractmethod
from src.domain.event import DomainEvent, AggregatedType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..legacy_user import LegacyUser


class LegacyUserEvent(DomainEvent):
    user: LegacyUser

    def __init__(self, user: LegacyUser):
        self.user: LegacyUser = user

    def aggregate_type(self) -> AggregatedType:
        return AggregatedType.USER

    def aggregate_id(self) -> int:
        return self.user.id

    def ower_id(self) -> int:
        return self.user.id

    @abstractmethod
    def occured_on(self) -> datetime.datetime: ...
