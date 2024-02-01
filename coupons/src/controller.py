from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

root_router = APIRouter(tags=['API'], prefix='/api/v1')


@root_router.post("")
def coupon_issurance():
    return JSONResponse(status_code=200, content={})
