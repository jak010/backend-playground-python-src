from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class LegacyAdGroup:
    id: Optional[int]
    name: str
    campaign_id: int
    user_id: int
    link_url: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    @classmethod
    def of(cls, name, campaign_id, user_id, link_url):
        return cls(
            id=None,
            name=name,
            campaign_id=campaign_id,
            user_id=user_id,
            link_url=link_url,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def update_name(self, name):
        self.name = name
        # TODO, 241130 : add domain event

    def update_linked_url(self, link_url):
        self.link_url = link_url
        # TODO, 241130 : add domain event

    def delete(self):
        self.deleted_at = datetime.now()
        # TODO, 241130 : add domain event
