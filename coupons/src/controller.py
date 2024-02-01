from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from src.service.coupon_service import CouPonIssueService

root_router = APIRouter(tags=['API'], prefix='/api/v1')


@root_router.post("")
def coupon_issurance():
    service = CouPonIssueService()
    service.issue_save()

    return JSONResponse(status_code=200, content={})
