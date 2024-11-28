from fastapi import APIRouter, Depends

from src.infrastructure.repositories.sqlalchemy_repository import ISqlalchemyRepository

index_router = APIRouter(prefix="/api/v1", tags=["INDEX"])


@index_router.get(path="")
def index_api(

):
    return {"message": "Hello World"}
