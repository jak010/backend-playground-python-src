from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

api_router = APIRouter(tags=['API'], prefix="/api/v1")


@api_router.post(
    path="",
)
def some_api():
    return JSONResponse(status_code=200, content={})
