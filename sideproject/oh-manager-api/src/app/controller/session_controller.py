from fastapi import APIRouter, Form, Depends

from src.app.controller.responses import s200, s404, s401, s400
from src.app.usecase.exceptions.member import DoesNotExistMember, DeactivateMember
from src.app.usecase.exceptions.validation import InvalidCredential
from src.app.usecase.authenticate.jwt_authenticate import JwtAuthenticate
from src.app.usecase.session import SessionCreateUseCase, SessionTerminateUseCase
from src.config.route import TransactionRoute

session_router = APIRouter(tags=['Session'], prefix="/api/session", route_class=TransactionRoute)


@session_router.post(
    path='',
    responses={
        400: {
            "content": {"application/json": {"examples": {
                "DEACTIVATE_MEMBER": {"value": s400.DeactivateMember.get_data()}
            }}}},
        401: {
            "content": {"application/json": {"examples": {
                "UNAUTHORIZED": {"value": s401.UnAuthorized.get_data()}
            }}}},
        404: {
            "content": {"application/json": {"examples": {
                "DOES_NOT_EXIST": {"value": s404.DoesNotExistMember.get_data()}
            }}}},
    }
)
def create_session(
        email: str = Form(),
        password: str = Form()
):
    try:
        access_token = SessionCreateUseCase.execute(email=email, password=password)
    except DoesNotExistMember:
        return s404.DoesNotExistMember()
    except InvalidCredential:
        return s401.UnAuthorized()
    except DeactivateMember:
        return s400.DeactivateMember()

    return s200.Normal(data={
        'access_token': access_token
    })


@session_router.delete(path='')
def terminate_session(
        session=Depends(JwtAuthenticate())
):
    SessionTerminateUseCase.execute(session)
    return s200.Normal(data={})
