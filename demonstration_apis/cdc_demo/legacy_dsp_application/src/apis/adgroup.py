from fastapi import APIRouter, Depends, Path

from src.domain.adgroup.legacy_adgroup_service import LegacyAdGroupService

from .schema.legacy_adgroup_schema import LegacyAdGroupCreateSchema, LegacyAdGroupUpdateSchema

legacy_adgroup_router = APIRouter(prefix="/api/v1/legacy-adgroup", tags=["LEGACY-ADGROUP"])


@legacy_adgroup_router.post(
    path="",
)
def create(
        request: LegacyAdGroupCreateSchema.LegacyAdGroupCreateRequest = Depends(LegacyAdGroupCreateSchema.LegacyAdGroupCreateRequest),
        service: LegacyAdGroupService = Depends(LegacyAdGroupService)
):
    return service.create(command=request)


@legacy_adgroup_router.delete(
    path="/{adgroup_id}",
)
def delete(
        adgroup_id: int = Path(),
        service: LegacyAdGroupService = Depends(LegacyAdGroupService)
):
    return service.delete(adgroup_id=adgroup_id)


@legacy_adgroup_router.get(
    path="/{adgroup_id}",
)
def find_by_id(
        adgroup_id: int = Path(),
        service: LegacyAdGroupService = Depends(LegacyAdGroupService)
):
    return service.find_by_id(adgroup_id=adgroup_id)


@legacy_adgroup_router.patch(
    path="/{adgroup_id}/name",
)
def update_name(
        request: LegacyAdGroupUpdateSchema.LegacyAdGroupUpdateNameRequest = Depends(
            LegacyAdGroupUpdateSchema.LegacyAdGroupUpdateNameRequest.as_body
        ),
        service: LegacyAdGroupService = Depends(LegacyAdGroupService)
):
    return service.update_name(adgroup_id=request.adgroup_id, name=request.name)


@legacy_adgroup_router.patch(path="/{adgroup_id}/link-url")
def update_link_url(
        request: LegacyAdGroupUpdateSchema.LegacyAdGroupUpdateLinkUrlRequest = Depends(
            LegacyAdGroupUpdateSchema.LegacyAdGroupUpdateLinkUrlRequest.as_body
        ),
        service: LegacyAdGroupService = Depends(LegacyAdGroupService)
):
    return service.update_linked_url(adgroup_id=request.adgroup_id, link_url=request.link_url)
