from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from .service import MemberService

member_router = APIRouter(tags=['API'], prefix="/api/v1/member")


@member_router.get("")
async def hello_world():
    s = MemberService()
    await s.call()

    return JSONResponse(status_code=200, content={})
