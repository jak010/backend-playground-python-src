from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LegacyCampaign(BaseModel):
    id: Optional[int]
    name: str
    user_id: int
    budget: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class LegacyCampignCreateSchema:
    class LegacyCampaignCreateRequest(BaseModel):
        name: str
        user_id: int
        budget: int

    class LegacyCampaignCreateResponse(LegacyCampaign): ...
