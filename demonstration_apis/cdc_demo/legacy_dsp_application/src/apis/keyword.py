from fastapi import APIRouter, Depends
from fastapi.params import Path

from src.domain.keyword.legacy_keyword_service import LegacyKeywordService
from .schema.legacy_keyword_schema import LegacyKeywordResponse, LegacyKeywordSchema, LegacyKeywordCreateSchema

legacy_keyword_router = APIRouter(prefix="/api/v1/legacy-keyword", tags=["LEGACY-KEYWORD"])


@legacy_keyword_router.post("", response_model=LegacyKeywordResponse)
def create(
        request: LegacyKeywordCreateSchema.LegacyKeywordCreateRequest = Depends(LegacyKeywordCreateSchema.LegacyKeywordCreateRequest),
        service: LegacyKeywordService = Depends(LegacyKeywordService)
):
    new_legacy_keyword = service.create(text=request.text, adgroup_id=request.adgroup_id, user_id=request.user_id)
    return LegacyKeywordResponse(**new_legacy_keyword.to_dict())


@legacy_keyword_router.get("", response_model=LegacyKeywordSchema.LegacyKeywordListResponse)
def find(
        service: LegacyKeywordService = Depends(LegacyKeywordService)
):
    return LegacyKeywordSchema.LegacyKeywordListResponse(
        data=[
            item.to_dict() for item in service.find()
        ]
    )


@legacy_keyword_router.delete("/{legacy_keyword_id}", response_model=LegacyKeywordSchema.LegacyKeywordDeleteResponse)
def delete(
        legacy_keyword_id: int = Path(),

        service: LegacyKeywordService = Depends(LegacyKeywordService)
):
    return LegacyKeywordSchema.LegacyKeywordDeleteResponse(**service.delete(pk=legacy_keyword_id).to_dict())
