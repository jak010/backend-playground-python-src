from fastapi import Depends, Path
from fastapi.responses import JSONResponse

from src.assessment.controller.request import AssessmentRequestFormDto
from src.assessment.usecase import AssessmentCompleteUseCase
from src.authenticate.usecase import JwtAuthenticate
from src.session.entity import SessionEntity
# from . import assessment_router


# @assessment_router.put(
#     path="/{nanoid:str}/approval",
#     description="Assessment Approval"
# )
# def member_agreement_service_update(
#         nanoid: str = Path(),
#         session: SessionEntity = Depends(JwtAuthenticate()),
#         request: AssessmentRequestFormDto = Depends(AssessmentRequestFormDto.as_form),
#         usecase: AssessmentCompleteUseCase = Depends(AssessmentCompleteUseCase)
#
# ):
#     usecase.execute(assessment_id=nanoid, reason=request.reason)
#     return JSONResponse(status_code=200, content={})
#
#
# @assessment_router.put(
#     path="/{nanoid:str}/reject",
#     description="Assessment Reject"
# )
# def member_agreement_service_update(
#         nanoid: str = Path(),
#         session: SessionEntity = Depends(JwtAuthenticate()),
#         request: AssessmentRequestFormDto = Depends(AssessmentRequestFormDto.as_form),
#         usecase: AssessmentCompleteUseCase = Depends(AssessmentCompleteUseCase)
# ):
#     usecase.execute(assessment_id=nanoid, reason=request.reason)
#
#     return JSONResponse(status_code=200, content={})
