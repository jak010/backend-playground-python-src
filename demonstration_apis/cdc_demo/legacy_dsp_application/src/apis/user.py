from fastapi import APIRouter, Depends
from fastapi.params import Path

from src.domain.user.legacy_user_service import LegacyUserService

from .schema.legacy_user_schema import LegacyUserCreateSchema, LegacyUserRetreieveSchema, LegacyUserDeleteSchema, LegacyUserUpdateSchema

legacy_user = APIRouter(prefix="/api/v1/legacy-user", tags=["LEGACY-USER"])


@legacy_user.post(
    path="",
    response_model=LegacyUserCreateSchema.LegacyUserCreateResponse
)
def create(
        request: LegacyUserCreateSchema.LegacyUserCreateRequest = Depends(LegacyUserCreateSchema.LegacyUserCreateRequest),
        service: LegacyUserService = Depends(LegacyUserService)
):
    new_user = service.create(name=request.name)
    return LegacyUserCreateSchema.LegacyUserCreateResponse(
        **new_user.to_dict()
    )


@legacy_user.get(
    path="/{user_id}",
    response_model=LegacyUserRetreieveSchema.LegacyUserFetchResponse
)
def find(
        request: LegacyUserRetreieveSchema.LegacyUserFetchRequest = Depends(LegacyUserRetreieveSchema.LegacyUserFetchRequest),
        service: LegacyUserService = Depends(LegacyUserService)
):
    search_user = service.search_legacy_user_by_id(user_id=request.user_id)
    return LegacyUserRetreieveSchema.LegacyUserFetchResponse(
        **search_user.to_dict()
    )


@legacy_user.patch(
    path="/{user_id}/name",
    response_model=LegacyUserUpdateSchema.LegacyUserUpdateNameResponse
)
def update_name(
        request: LegacyUserUpdateSchema.LegacyUserUpdateNameRequest = Depends(LegacyUserUpdateSchema.LegacyUserUpdateNameRequest.as_body),
        service: LegacyUserService = Depends(LegacyUserService)
):
    search_user = service.update_name(user_id=request.user_id, name=request.name)
    return LegacyUserUpdateSchema.LegacyUserUpdateNameResponse(
        **search_user.to_dict()
    )


@legacy_user.delete(
    path="/{user_id}",
)
def delete(
        request: LegacyUserDeleteSchema.LegacyUserRemoveRequest = Depends(LegacyUserDeleteSchema.LegacyUserRemoveRequest),
        service: LegacyUserService = Depends(LegacyUserService)
):
    service.delete_legacy_user_by_id(user_id=request.user_id)
    return {"result": "success"}
