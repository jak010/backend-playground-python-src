from fastapi import APIRouter, Depends, Form
from pydantic import Field
from src.app.controller.responses import s200, s400
from src.app.domain.member.member_entity import MemberEntity
from src.app.usecase.exceptions.validation import InvalidSubmissions, InvalidAuditions
from src.app.usecase.authenticate.jwt_authenticate import JwtAuthenticate
from src.app.usecase.submission_usecase import SubmissionsApplyUseCase, ReadSubmissionListUseCase
from src.config.route import TransactionRoute

submission_router = APIRouter(tags=['SUBMISSION'], prefix="/api/submissions", route_class=TransactionRoute)


@submission_router.get(
    path="",
    responses={
        200: {
            "content": {"application/json": {"example": {"items": [{
                "submission": {
                    "status": 'str',
                    "created_at": 'int',
                },
                "auditions": {
                    "title": "str",
                    "content": "str",
                    "category": 'str',
                    "reward": 'str',
                    "end_date": 'datetime.datetime.isoformat'
                }
            }
            ]}}}
        }
    }
)
def submissions_list(
        session: MemberEntity = Depends(JwtAuthenticate())
):
    """ 오디션 제출 목록조회 """
    return s200.Normal(data=ReadSubmissionListUseCase.execute(session=session))


@submission_router.post(
    path="",
    responses={
        400: {
            "content": {"application/json": {"examples": {
                "INVALID_AUDITION": {"value": s400.InvalidAudition.get_data()},
                "SUBMISSION_FAILURE": {"value": s400.SubmissionFailure.get_data()},
            }}}},
    }
)
def submissions_apply(
        session: MemberEntity = Depends(JwtAuthenticate()),
        audition_id: int = Form()
):
    """ 오디션 제출 """
    try:
        SubmissionsApplyUseCase.execute(
            session=session,
            audition_id=audition_id
        )
    except InvalidAuditions:
        return s400.InvalidAudition()
    except InvalidSubmissions:
        return s400.SubmissionFailure()

    return s200.Normal(data={})
