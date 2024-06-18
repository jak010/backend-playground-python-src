from fastapi import Form, Depends
from fastapi.responses import JSONResponse

from libs.utils.token_utils import SessionToken
from src.session.entity import SessionEntity
from settings.config.base import ExecuteEnviorment
from src.authenticate.usecase import (
    ServiceAgreementPolicyAuthenticate
)
from src.certification.controller import ceritifcation_router
from src.certification.controller.responses import s400, s404
from src.certification.usecase import (
    SmsCerificationRequestUseCase,
    AlredaySmsCerificationRequestException,
    AlreadyCerificationCompleteException,
    SmsCerificationVerifyUseCase,
    CertificationDoesNotExist
)


@ceritifcation_router.post(
    path="/sms/request",
    description=" Certificate, SMS",
    responses={
        400: {
            "content": {"application/json": {"examples": {
                "AlredaySmsCerificationCeomplete": {"value": s400.AlredaySmsCerificationCeompleteResponse.body()},
                "AlredaySmsCerificationRequest": {"value": s400.AlredaySmsCerificationRequestResponse.body()}
            }}}
        }
    }
)
def sms_certificate_request(
        session: SessionEntity = Depends(ServiceAgreementPolicyAuthenticate()),
        usecase: SmsCerificationRequestUseCase = Depends(SmsCerificationRequestUseCase)
):
    try:
        cerfication = usecase.execute(session=session)
    except AlreadyCerificationCompleteException:
        return s400.AlredaySmsCerificationCeompleteResponse()
    except AlredaySmsCerificationRequestException:
        return s400.AlredaySmsCerificationRequestResponse()

    if ExecuteEnviorment.MODE == 'LOCAL' or ExecuteEnviorment.MODE == 'DEV':
        return JSONResponse(status_code=200, content={
            'code': cerfication.code
        })

    return JSONResponse(status_code=200, content={})


@ceritifcation_router.post(
    path="/sms",
    description=" Certificate, SMS",
    responses={
        404: {
            "content": {"application/json": {"examples": {
                "NotFoundSmsCerificationCode": {"value": s404.NotFoundSmsCerificationCode.body()},

            }}}
        }
    }
)
def sms_certificate_verify(
        session: SessionToken = Depends(ServiceAgreementPolicyAuthenticate()),
        sms_code: str = Form(),
        usecase: SmsCerificationVerifyUseCase = Depends(SmsCerificationVerifyUseCase)
):
    try:
        usecase.execute(session=session, sms_code=sms_code)
    except CertificationDoesNotExist:
        return s404.NotFoundSmsCerificationCode()

    return JSONResponse(status_code=200, content={})
