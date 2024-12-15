from fastapi.routing import APIRouter

index_router = APIRouter(tags=["INDEX"], prefix="/api/v1/index")


@index_router.get(path="")
def index():
    return "Hello World"
