from __future__ import annotations

from typing import Optional
from dataclasses import dataclass, field, asdict

from datetime import datetime

from src.domain.abstract_aggregate_root import AbstactAggregateRoot

from .event.legacy_user_updated_name_event import LegacyUserUpdatedNamedEvent


@dataclass
class LegacyUser(AbstactAggregateRoot["LegacyUser"]):
    id: Optional[int] = field(default=None)
    name: str = field(default=None)

    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())
    deleted_at: Optional[datetime] = None

    @classmethod
    def of(cls, name: str):
        return cls(name=name)

    def update_name(self, name):
        # TODO, 241128 : add Domain Event
        self.name = name
        self.updated_at = datetime.now()

        # Event Published
        self.register_event(
            LegacyUserUpdatedNamedEvent(self)
        )

    def delete(self):
        # TODO, 241128 : add Domain Event
        self.deleted_at = datetime.now()

    def to_dict(self):
        return asdict(self)
