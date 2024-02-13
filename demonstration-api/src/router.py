from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from settings.dev import get_db

api_router = APIRouter(tags=['API'], prefix="/api/v1")


@api_router.post(path="/")
def some_api(
        session: Session = Depends(get_db)
):
    with session.begin():
        session.execute("select 1")
        session.commit()

    return JSONResponse(status_code=200, content={})
