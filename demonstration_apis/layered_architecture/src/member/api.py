from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from src.member.exceptions import (
    AlreadyExistMember,
    MemberNotFound
)
from src.member.service import MemberService

member_router = APIRouter(tags=['MEMBER'], prefix="/api/v1/member")


@member_router.get(path="/{member_id}")
def get_member(
        member_id: int = Path(),
        service: MemberService = Depends(MemberService)
):
    try:
        service.get_member(member_id=member_id)
    except MemberNotFound:
        return JSONResponse(status_code=400, content={})
    return JSONResponse(status_code=200, content={})


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
