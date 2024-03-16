from fastapi import Depends, Body
from fastapi import Path
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from src.domain.entity.member_entity import MemberEntity
from src.domain.entity.member_profile_entity import MemberProfileEntity
from src.infra.repository import MemberRepositry, MemberProfileRepository

api_router = APIRouter(tags=['RELATION'], prefix="/api/v1")


@api_router.post(
    path="/member"
)
def member_create(
        name: str = Body(),
        age: int = Body(),

        member_repository: MemberRepositry = Depends(MemberRepositry),
        member_profile_repository: MemberProfileRepository = Depends(MemberProfileRepository)
):
    member_entity = MemberEntity.new(
        name=name,
        age=age
    )

    member_profile = MemberProfileEntity.by(member=member_entity, description="test")

    member_repository.save(member_entity)
    member_profile_repository.save(member_profile)

    return JSONResponse(status_code=200, content={})


@api_router.get(
    path="/member/{member_id}"
)
def member_read(
        member_id: str = Path(),
        repository: MemberRepositry = Depends(MemberRepositry)
):
    aggrage = repository.find_by_member_id(member_id=member_id)

    return JSONResponse(status_code=200, content={})


