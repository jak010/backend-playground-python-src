from dataclasses import dataclass, asdict
from typing import Optional

from datetime import datetime


@dataclass
class LegacyCampaign:
    id: Optional[int]
    name: str
    user_id: int
    budget: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    @classmethod
    def of(cls, name, user_id, budget):
        return cls(
            id=None,
            name=name,
            user_id=user_id,
            budget=budget,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def update_name(self, name):
        # TODO, 241128 : add Domain Event
        self.name = name
        self.updated_at = datetime.now()

    def update_budget(self, budget):
        # TODO, 241128 : add Domain Event
        self.budget = budget

    def delete(self):
        # TODO, 241128 : add Domain Event
        self.deleted_at = datetime.now()

    def to_dict(self):
        return asdict(self)
