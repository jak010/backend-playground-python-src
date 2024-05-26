from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")


class SuccessResponseModel(BaseModel, Generic[T]):
    status_code: int
    data: T


class PaginateResponseModel(BaseModel, Generic[T]):
    status_code: int
    page: int
    per_page: int
    total_count: int
    data: List[T]
