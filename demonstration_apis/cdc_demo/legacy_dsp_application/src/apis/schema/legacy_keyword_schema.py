from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class LegacyKeywordResponse(BaseModel):
    id: Optional[int]
    text: str
    adgroup_id: int
    user_id: int
    created_at: datetime
    deleted_at: Optional[datetime] = None


class LegacyKeywordCreateSchema:
    class LegacyKeywordCreateRequest(BaseModel):
        text: str
        adgroup_id: int
        user_id: str


class LegacyKeywordSchema:
    class LegacyKeywordListResponse(BaseModel):
        data: List[LegacyKeywordResponse]

    class LegacyKeywordDeleteResponse(LegacyKeywordResponse): ...
