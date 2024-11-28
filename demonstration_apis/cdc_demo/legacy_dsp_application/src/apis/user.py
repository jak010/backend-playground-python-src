from fastapi import APIRouter, Depends

from src.domain.user.legacy_user_service import LegacyUserService

legacy_user = APIRouter(prefix="/api/v1/legacy-user", tags=["INDEX"])


@legacy_user.post(path="")
def create(
        service: LegacyUserService = Depends(LegacyUserService)
):
    service.create(name="test")

    return {"message": "Hello World"}
