from fastapi import APIRouter, Depends

from src.domain.campaign.legacy_campaign_service import LegacyCampignService
from .schema.legacy_campaign_shcema import LegacyCampignCreateSchema

legacy_campaign_router = APIRouter(prefix="/api/v1/legacy-campaign", tags=["LEGACY-CAMPAIGN"])


@legacy_campaign_router.get(
    path="",
)
def find(
        service: LegacyCampignService = Depends(LegacyCampignService)
):
    service.find_by_id(campaign_id=1)
    return {"message": "Hello World"}


@legacy_campaign_router.post(
    path="",
    response_model=LegacyCampignCreateSchema.LegacyCampaignCreateResponse
)
def create(
        request: LegacyCampignCreateSchema.LegacyCampaignCreateRequest,
        service: LegacyCampignService = Depends(LegacyCampignService)
):
    saved_campign = service.create(name=request.name, user_id=request.user_id, budget=request.budget)

    return LegacyCampignCreateSchema.LegacyCampaignCreateResponse(
        **saved_campign.to_dict()
    )
