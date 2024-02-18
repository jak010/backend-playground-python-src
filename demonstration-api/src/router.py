import requests.utils
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from src.repository import Repository

api_router = APIRouter(tags=['API'], prefix="/api/v1")


# @api_router.post(path="/")
# async def some_api(
#         session: Session = Depends(get_db)
# ):
#     session.execute("select 1")
#     session.commit()
#     session.close()
#
#     return JSONResponse(status_code=200, content={})


@api_router.post(path="/session/example")
def repository_session_example2():
    repo = Repository()
    repo.get_session()

    return JSONResponse(status_code=200, content={})
