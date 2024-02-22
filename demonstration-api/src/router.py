from fastapi import Depends, Body
from fastapi import Path
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from core.entity.member_entity import MemberEntity
from core.entity.member_profile_entity import MemberProfileEntity
from core.repository import MemberRepositry, MemberProfileRepository

api_router = APIRouter(tags=['API'], prefix="/api/v1")


@api_router.post(
    path="/member"
)
def example_create_member(
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
    path="/member/{nanoid}"
)
def example_get_member(
        nanoid: str = Path(),

        repository: MemberRepositry = Depends(MemberRepositry)

):
    member = repository.get(nanoid=nanoid)

    return JSONResponse(status_code=200, content={})
