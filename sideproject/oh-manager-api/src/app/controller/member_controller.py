from typing import Literal

from fastapi import APIRouter, Depends, Form

from src.app.controller.responses import s200, s400
from src.app.domain.member.member_entity import MemberEntity
from src.app.usecase.authenticate.jwt_authenticate import JwtAuthenticate
from src.app.usecase.member_useacse import MemberReadUseCase, MemberCategoryUpdateUsecase, MemberCategoryDuplicate
from src.config.route import TransactionRoute

member_router = APIRouter(tags=['MEMBER'], prefix="/api/member", route_class=TransactionRoute)


@member_router.get(
    path="",
    response_model=s200.ResponseModel[MemberEntity]
)
def retreieve_member(
        session=Depends(JwtAuthenticate()),
):
    # TODO 2024.01.25: s200 문서 작업 필요
    member_aggregate = MemberReadUseCase.execute(session=session)

    return s200.Normal(
        data=member_aggregate.read()
    )


@member_router.post(
    path="/category",
    responses={
        400: {
            "content": {"application/json": {"examples": {
                "DUPLICATE_MEMBER_CATEGORY": {"value": s400.DuplicateMemberCategory.get_data()}
            }}}},
    }
)
def insert_category(
        session=Depends(JwtAuthenticate()),
        primary: Literal["가수", "영화", "모델"] = Form(),
        secondary: str = Form(default=None)
):
    try:
        MemberCategoryUpdateUsecase.execute(
            session=session,
            primary=primary,
            secondary=secondary
        )
    except MemberCategoryDuplicate as e:
        return s400.DuplicateMemberCategory()

    return s200.Normal(data={})
