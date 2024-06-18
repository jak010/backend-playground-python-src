from fastapi import Depends
from fastapi.responses import JSONResponse

from src.authenticate.usecase.authenticate_expire_usecase import AuthenticateExpireUseCase
from src.authenticate.usecase.jwt_authenticate import JwtAuthenticate
from src.session.entity import SessionEntity

from . import authenticate_router


@authenticate_router.delete(
    path="",
    description="Authenticate Exipre"
)
def authentication_terminate(
        session: SessionEntity = Depends(JwtAuthenticate()),
        usecase: AuthenticateExpireUseCase = Depends(AuthenticateExpireUseCase)
):
    usecase.execute(session=session)

    return JSONResponse(status_code=200, content={})
