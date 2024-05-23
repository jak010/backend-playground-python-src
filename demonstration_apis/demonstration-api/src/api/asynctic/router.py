import motor.motor_asyncio
from starlette.responses import JSONResponse

from fastapi.routing import APIRouter
from .repository import DocumentDBRepository
from fastapi import Depends

mongodb_router = APIRouter(tags=['MongoDB'], prefix="/api/v1/mongodb")


@mongodb_router.get(
    path=""
)
async def ex1(
        repository: DocumentDBRepository = Depends(DocumentDBRepository)

):
    r = await repository.find_by_id(123)

    print(r)

    return JSONResponse(status_code=200, content={})
