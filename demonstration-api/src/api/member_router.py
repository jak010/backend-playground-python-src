from fastapi import Depends, Body
from fastapi import Path
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from src.domain.entity.member_entity import MemberEntity
from src.domain.entity.member_profile_entity import MemberProfileEntity
from src.infra.repository import MemberRepositry, MemberProfileRepository

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
    path="/member/{member_id}"
)
def example_get_member(
        member_id: str = Path(),
        repository: MemberRepositry = Depends(MemberRepositry)
):
    aggrage = repository.find_by_member_id(member_id=member_id)

    return JSONResponse(status_code=200, content={})


@api_router.get(
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


@api_router.post(
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
        address=Address(
            address1='address1-1',
            address2='address2-1'
        )
    )

    member_repository.save(member_entity=member_entity)

    return JSONResponse(status_code=200, content={})


@api_router.get(
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
    print(member_entity.address)
    print("=" * 20)

    return JSONResponse(status_code=200, content={})
