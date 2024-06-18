from fastapi import Depends, Path
from fastapi.responses import JSONResponse

from src.authenticate.usecase import JwtAuthenticate
from src.session.entity import SessionEntity
from src.social.controller.request import SocialInviteRequestDto, SocialInviteList
from src.social.controller.response import s400
from src.social.usecase.exceptions import *
from src.social.usecase.social_invite_approval_usecase import SocialInviteApprovalUsecase
from src.social.usecase.social_invite_reject_usecase import SocialInviteRejectUsecase
from src.social.usecase.social_invite_read_usecase import SocialInviteReadUsecase
from src.social.usecase.social_invite_request_usecase import (
    SocialInviteRequestUsecase
)
from . import social_router


@social_router.get(
    path="/social-invite",
    description="Social, Invtie List API ",
    response_model=SocialInviteList
)
def social_invite_request(
        session: SessionEntity = Depends(JwtAuthenticate()),
        usecase: SocialInviteReadUsecase = Depends(SocialInviteReadUsecase)
):
    social_invite_list = usecase.execute(session=session)

    return JSONResponse(
        status_code=200,
        content=social_invite_list.model_dump()
    )


@social_router.post(
    path="/social-invite/request",
    description="Social, Invtie Request API",
    responses={
        400: {
            "content": {"application/json": {"examples": {
                "NotFoundReceiverMember": {"value": s400.InvalidReceiverMember.body()},
                "AlreadyRequestInvtide": {"value": s400.AlreadyRequestInvited.body()}
            }}}
        }
    }
)
def social_invite_request(
        session: SessionEntity = Depends(JwtAuthenticate()),
        request: SocialInviteRequestDto = Depends(SocialInviteRequestDto.as_form),
        usecase: SocialInviteRequestUsecase = Depends(SocialInviteRequestUsecase)
):
    try:
        usecase.execute(session=session, request=request)
    except NotFoundReceiverMember:
        return s400.InvalidReceiverMember()
    except AlreadyRequestInvited:
        return s400.AlreadyRequestInvited()

    return JSONResponse(status_code=200, content={})


@social_router.post(
    path="/social-invite/{social_id}/approval",
    description="Social, Invtie Request Approval API",
    responses={
        400: {
            "content": {"application/json": {"examples": {
                "AlreadySocialApproval": {"value": s400.AlreadySocialApproval.body()}
            }}}
        }
    }
)
def social_invite_approval(
        social_id: int = Path(),

        session: SessionEntity = Depends(JwtAuthenticate()),
        usecase: SocialInviteApprovalUsecase = Depends(SocialInviteApprovalUsecase)
):
    try:
        usecase.execute(session=session, social_id=social_id)
    except AlreadySocialApproval:
        return s400.AlreadySocialApproval()

    return JSONResponse(status_code=200, content={})


@social_router.post(
    path="/social-invite/{social_id}/reject",
    description="Social, Invtie Request Reject API",
    responses={
        400: {
            "content": {"application/json": {"examples": {
                "InvalidSocialInvitedRequest": {"value": s400.InvalidSocialInvitedRequest.body()}
            }}}
        }
    }
)
def social_invite_approval(
        social_id: int = Path(),

        session: SessionEntity = Depends(JwtAuthenticate()),
        usecase: SocialInviteRejectUsecase = Depends(SocialInviteRejectUsecase)
):
    try:
        usecase.execute(session=session, social_id=social_id)
    except InvalidSocialInviteRequested:
        return s400.InvalidSocialInvitedRequest()

    return JSONResponse(status_code=200, content={})
