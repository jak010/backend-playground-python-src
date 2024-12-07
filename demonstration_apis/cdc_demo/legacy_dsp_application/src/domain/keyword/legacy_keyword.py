from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime


@dataclass
class LegacyKeyword:
    id: Optional[int]
    text: str
    adgroup_id: int
    user_id: int
    created_at: datetime
    deleted_at: Optional[datetime]

    @classmethod
    def of(cls, text, adgroup_id, user_id):
        return cls(
            id=None,
            text=text,
            adgroup_id=adgroup_id,
            user_id=user_id,
            created_at=datetime.now(),
            deleted_at=None
        )

    def delete(self):
        if self.deleted_at is not None:
            raise Exception("Already Deleted")
        self.deleted_at = datetime.now()
        return self

    def to_dict(self):
        return asdict(self)
