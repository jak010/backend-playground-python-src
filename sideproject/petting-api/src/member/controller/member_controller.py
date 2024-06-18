from fastapi import Depends
from fastapi.responses import JSONResponse

from src.authenticate.usecase import JwtAuthenticate
from src.member.controller.request import RequestMemberTemsrOfAgreementsFormDTO
from src.member.usecase.member_aggrement_service_update_usecase import MemberServiceAggrementUpdateUseCase
from src.session.entity import SessionEntity
from . import member_router


@member_router.put(
    path="/agreement-service",
    description="Member, Service Terms Agreement Update"
)
def member_agreement_service_update(
        session: SessionEntity = Depends(JwtAuthenticate()),
        request: RequestMemberTemsrOfAgreementsFormDTO = Depends(RequestMemberTemsrOfAgreementsFormDTO.as_form),
        usecase: MemberServiceAggrementUpdateUseCase = Depends(MemberServiceAggrementUpdateUseCase)
):
    usecase.execute(session=session, request=request)
    return JSONResponse(status_code=200, content={})
