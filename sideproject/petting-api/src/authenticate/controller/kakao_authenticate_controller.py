from fastapi import Depends, Query
from fastapi.responses import JSONResponse, RedirectResponse

from src.authenticate.controller.response import s400
from src.authenticate.usecase.kakao_authenticate import (
    KaKaoOauthAuthorizedCodeUseCase,
    KaKaoAuthenticateUseCase,
    KaKaoAuthenticateFailureException
)
from . import kakao_oauth_router


@kakao_oauth_router.get(
    path="/authorization",
    description="KaKao, Authorized",
    responses={
        200: {
            "content": {"application/json": {"examples": {
                "Normal": {"value": "Redriect(status_code:307)"}
            }}}
        }
    }
)
def kakao_authorization(
        usecase: KaKaoOauthAuthorizedCodeUseCase = Depends()
):
    """ Kakao Oauth, Authorized(http://127.0.0.1:8000/api/v1/oauth/kakao/authorization)"""
    return RedirectResponse(usecase.execute())


@kakao_oauth_router.get(
    path="/authenticate",
    description="KaKao, Authenticate",
    responses={
        200: {
            "content": {"application/json": {"examples": {
                "Normal": {"value": {"access-token": "string"}}
            }}}
        },
        400: {
            "content": {"application/json": {"examples": {
                "KaKaoAuthenticateFailureResponse": {"value": s400.KaKaoAuthenticateFailureResponse.body()}
            }}}
        },
    }
)
def kako_authenticate(
        code: str = Query(),
        usecase: KaKaoAuthenticateUseCase = Depends(),
):
    """ Kakao Oauth, Authorized """
    try:
        session_token = usecase.execute(authorization_code=code)
    except KaKaoAuthenticateFailureException as e:
        return s400.KaKaoAuthenticateFailureResponse()

    return JSONResponse(
        status_code=200,
        content={
            "access-token": session_token.generate_token()
        }
    )
