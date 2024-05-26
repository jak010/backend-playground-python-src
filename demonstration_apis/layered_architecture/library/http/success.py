from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")


class BaseResponseModel(BaseModel, Generic[T]):
    status_code: int
    data: T


class PaginateResponseModel(BaseModel, Generic[T]):
    status_code: int
    page: int
    per_page: int
    total_count: int
    data: List[T]


class BaseSuccessResponse(JSONResponse):
    STATUS_CODE: int = None
    DATA: str = None

    def __init__(self, data):
        self.data = data
        super().__init__(
            status_code=self.STATUS_CODE,
            content=self.body()
        )

    @classmethod
    def body(cls):
        return {
            "status_code": cls.STATUS_CODE,
            "data": cls.DATA
        }


class Normal(BaseSuccessResponse):
    STATUS_CODE = 200
