from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from .service_pattern import example01
import os
import threading

asyncio_router = APIRouter(tags=['ASYNCIO'], prefix="/api/v1/asyncio")


@asyncio_router.get(
    path='/v1'
)
def router_example01():
    print(threading.get_ident())

    return JSONResponse(status_code=200, content={})


@asyncio_router.get(
    path=''
)
async def router_example01():
    print(threading.get_ident())
    # while True:
    #     print(os.getpid())

    return JSONResponse(status_code=200, content={})
