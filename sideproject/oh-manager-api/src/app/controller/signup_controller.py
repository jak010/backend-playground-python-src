from fastapi import APIRouter, Form

from src.app.controller.responses import s400, s200, s404
from src.app.controller.responses.s400 import AlreadyJoinedMember
from src.app.usecase.exceptions.member import AlreadyJoinedMember, AlreadyExistEmail
from src.app.usecase.exceptions.validation import InvalidEmail
from src.app.usecase.exceptions.verification import (
    VerificationCodeExpired,
    VerificationCodeIsNotPending,
    DoesNotExistVerification
)
from src.app.usecase.signup import SignUpVerificationUsecase, SignUpRequestUsecase
from src.config.route import TransactionRoute

signup_router = APIRouter(tags=['SIGNUP'], prefix="/api/signup", route_class=TransactionRoute)


@signup_router.post(
    path="/request",
    responses={
        200: {
            "content": {"application/json": {"example": {"result": "success"}}}
        },
        400: {
            "content": {
                "application:json": {
                    "examples": {
                        "INVALIDE EMAIL": {"value": s400.InvalidEmail.get_data()},
                        "ALREADY EXIST EAMIL": {"value": s400.AlreadyExistEmail.get_data()}
                    }}
            }
        },
    }
)
def signup(
        email: str = Form(),
        password: str = Form()
):
    try:
        SignUpRequestUsecase.execute(
            member_email=email,
            member_password=password
        )
    except InvalidEmail as e:
        return s400.InvalidEmail()
    except AlreadyExistEmail as e:
        return s400.AlreadyExistEmail()

    return s200.Normal(
        data={
            "message": "Send Verification Code, Please Check Email"
        }
    )


@signup_router.post(
    path="/verification",
    responses={
        400: {
            "content": {"application/json": {"examples": {
                "VERIFICATION_CODE_EXPIRED": {"value": s400.VerificationCodeExpired.get_data()},
                "VERIFICATION_CODE_IS_NOT_PENDING": {"value": s400.VerificationCodeIsNotPending.get_data()},
                "ALREADY_JOINED_MEMBER": {'value': s400.AlreadyJoinedMember.get_data()}
            }}}},
        404: {
            "content": {"application/json": {"examples": {
                "DOES_NOT_EXIST_VERIFICATION": {"value": s404.DoesNotExsitVerification.get_data()}
            }}}}
    }
)
def signup_verification(
        verification_code: str = Form()
):
    try:
        new_member = SignUpVerificationUsecase.execute(
            verification_code=verification_code
        )
    except DoesNotExistVerification:
        return s404.DoesNotExsitVerification()
    except VerificationCodeExpired:
        return s400.VerificationCodeExpired()
    except VerificationCodeIsNotPending:
        return s400.VerificationCodeIsNotPending()
    except AlreadyJoinedMember:
        return s400.AlreadyJoinedMember()

    return s200.Normal(
        data={
            "member_id": new_member.id,
            "email": new_member.email,
            "joined_at": new_member.joined_at,
            "created_at": new_member.joined_at
        }
    )


@signup_router.post(path="/retry")
def signup_code_resned(
        email: str = Form(())
):
    # TODO 24.01.19, 구현 필요함
    return s200.Normal(data={})
