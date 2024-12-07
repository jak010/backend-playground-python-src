from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.domain.keyword.legacy_keyword_service import LegacyKeywordService

legacy_keyword_router = APIRouter(prefix="/api/v1/legacy-keyword", tags=["LEGACY-KEYWORD"])


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


@legacy_keyword_router.post("", response_model=LegacyKeywordResponse)
def create(
        request: LegacyKeywordCreateSchema.LegacyKeywordCreateRequest = Depends(LegacyKeywordCreateSchema.LegacyKeywordCreateRequest),
        service: LegacyKeywordService = Depends(LegacyKeywordService)
):
    new_legacy_keyword = service.create(text=request.text, adgroup_id=request.adgroup_id, user_id=request.user_id)
    return LegacyKeywordResponse(**new_legacy_keyword.to_dict())
