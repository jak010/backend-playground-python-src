from fastapi.responses import JSONResponse

from .index_router import index_router_v1


@index_router_v1.get(path="/sub")
def some_router():
    return JSONResponse(status_code=200, content={})
