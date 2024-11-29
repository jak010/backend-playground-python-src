from typing import Optional
from dataclasses import dataclass, field, asdict

from datetime import datetime


@dataclass
class LegacyUser:
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

    def delete(self):
        # TODO, 241128 : add Domain Event
        self.deleted_at = datetime.now()

    def to_dict(self):
        return asdict(self)
