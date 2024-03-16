from fastapi import Depends
from fastapi import Path
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from src.infra.repository import MemberRepositry, MemberProfileRepository

api_router_many_to_one = APIRouter(tags=['RELATION'], prefix="/api/v1/member")


@api_router_many_to_one.get("/{member_id}/with-profile")
def read_member_with_profile(
        member_id: str = Path(),
        member_repository: MemberRepositry = Depends(MemberRepositry),
        member_profile_repository: MemberProfileRepository = Depends(MemberProfileRepository)
):
    member_aggregate = member_repository.find_by_member_with_profile(member_id=member_id)

    member_aggregate.root_entity.name = 'update_1'
    member_aggregate.profile[0].description = 'update_description_1'
    member_aggregate.profile[1].description = 'update_description_2'

    member_repository.insert(member_aggregate)

    return JSONResponse(status_code=200, content={})
