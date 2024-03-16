from fastapi import APIRouter
from fastapi.responses import JSONResponse

redis_lock_test_router = APIRouter(tags=['REDIS_LOCK'], prefix='/api/v1/redis')


@redis_lock_test_router.get(path="")
def redis_loca():
    return JSONResponse(status_code=200, content={})
