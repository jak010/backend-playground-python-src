from fastapi import Depends, Body
from fastapi import Path
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from src.domain.entity.member_entity import MemberEntity
from src.domain.entity.member_profile_entity import MemberProfileEntity
from src.infra.repository import MemberRepositry, MemberProfileRepository

api_router_value_object = APIRouter(tags=['VALUE_OBJECT'], prefix="/api/v1")


@api_router_value_object.get(
    path="/member/{member_id}/value-object"
)
def example_get_member(
        member_id: str = Path(),

        member_repository: MemberRepositry = Depends(MemberRepositry),
        member_profile_repository: MemberProfileRepository = Depends(MemberProfileRepository)

):
    from src.domain.value_object.address import Address

    member_entity = MemberEntity.new(name=12, age=10, address=Address(address1="test-address1", address2="test-address2"))

    member_profile_entity = MemberProfileEntity.by(member=member_entity, description="test")

    member_repository.save(member_entity=member_entity)
    member_profile_repository.save(member_profile_entity=member_profile_entity)

    return JSONResponse(status_code=200, content={})


@api_router_value_object.post(
    path="/member/value-object"
)
def example_get_member(

        member_repository: MemberRepositry = Depends(MemberRepositry),
        member_profile_repository: MemberProfileRepository = Depends(MemberProfileRepository)

):
    from src.domain.value_object.address import Address

    member_entity = MemberEntity.new(
        name="test",
        age=123,
    )

    member_repository.save(member_entity=member_entity)

    return JSONResponse(status_code=200, content={})


@api_router_value_object.get(
    path="/member/{member_id}/value-object/find"
)
def example_get_member(
        member_id: str = Path(),

        member_repository: MemberRepositry = Depends(MemberRepositry),
        member_profile_repository: MemberProfileRepository = Depends(MemberProfileRepository)

):
    from src.domain.value_object.address import Address

    member_entity = member_repository.find_by_member_id(member_id=member_id)
    print("=" * 20)
    print(dir(member_entity))
    print("-" * 20)
    print(member_entity)
    # print(member_entity.address)
    print("=" * 20)

    return JSONResponse(status_code=200, content={})
