from fastapi import Depends, Body
from fastapi import Path
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from src.domain.member.entity import MemberEntity, MemberProfileEntity
from src.infra.repository import MemberRepositry, MemberProfileRepository, IRepository, Repository

proxysql_api_router = APIRouter(tags=['PROXYSQL'], prefix="/api/v1")


@proxysql_api_router.get("/test")
def get_connection(
        repository: Repository = Depends(Repository)
):
    repository.session.execute("select * from tb_test;")
    repository.session.commit()
    repository.session.close()

    return JSONResponse(status_code=200, content={})
