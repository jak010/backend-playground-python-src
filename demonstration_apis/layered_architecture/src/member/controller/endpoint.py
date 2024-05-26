from typing import List

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from library.http.models import PaginateResponseModel, SuccessResponseModel
from src.member.controller.responses import s404, s200
from src.member.controller.responses.schema import MemberResponseModel
from src.member.service.exceptions import (
    AlreadyExistMember,
    MemberNotFound
)
from src.member.service.member_service import MemberService
from external_library.orm import Member

member_router = APIRouter(tags=['MEMBER'], prefix="/api/v1/member")


@member_router.get(
    path="",
    response_model=PaginateResponseModel[MemberResponseModel],
)
def get_member(
        service: MemberService = Depends(MemberService)
):
    try:
        members: List[Member] = service.get_members()
    except MemberNotFound:
        return s404.MemberNotFound()

    return s200.MemberPaginateResponse(
        page=0,
        per_page=0,
        total_count=10,
        data=[{
            "pk": member.pk,
            "name": member.name,
            "age": member.age
        } for member in members]
    )


@member_router.get(
    path="/{member_id}",
    response_model=SuccessResponseModel[MemberResponseModel],
    responses={
        400: {
            "content": {"application/json": {"examples": {
                "MemberNotFound": {"value": s404.MemberNotFound.body()},
            }}}
        },
    },

)
def get_member(
        member_id: int = Path(),
        service: MemberService = Depends(MemberService)
):
    try:
        member = service.get_member(member_id=member_id)
    except MemberNotFound:
        return s404.MemberNotFound()
    return s200.Normal(data=MemberResponseModel.model_dump(**member))


@member_router.post(path="")
def create_member(
        name: str,
        age: int,
        service: MemberService = Depends(MemberService)
):
    try:
        service.register(name=name, age=age)
    except AlreadyExistMember:
        return JSONResponse(status_code=400, content={})

    return JSONResponse(status_code=200, content={})
