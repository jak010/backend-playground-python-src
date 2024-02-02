from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field

from config.logger import UVICORN_SYSOUT_LOGGER
from src.service.coupon_service import CouPonIssueService

from src.entity.coupon_entity import CouponIssueException

root_router = APIRouter(tags=['API'], prefix='/api/v1')


class CoutponIssueRequestDto(BaseModel):
    user_id: int = Field()
    coupon_id: int = Field()


@root_router.post(path="")
def coupon_issurance(
        request: CoutponIssueRequestDto,
        service: CouPonIssueService = Depends(CouPonIssueService)
):
    try:
        service.issue(coupon_id=request.coupon_id, user_id=request.user_id)
    except CouponIssueException as e:
        return JSONResponse(status_code=200, content={
            "is_success": False,
            "message": e.message
        })

    UVICORN_SYSOUT_LOGGER.debug(f"쿠폰 발급 완료. coupon_id:{request.coupon_id}, user_id:{request.user_id}")

    return JSONResponse(status_code=200, content={})
