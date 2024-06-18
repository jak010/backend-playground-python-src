from typing import Generic, TypeVar, Optional

from fastapi.responses import JSONResponse as _JSONResponse
from pydantic import BaseModel, Field

T = TypeVar("T")


class Normal(_JSONResponse):
    STATUS_CODE = 200
    CODE = 20000

    def __init__(self, data: dict):
        super().__init__(
            status_code=self.STATUS_CODE,
            content=data
        )


class ResponseModel(BaseModel, Generic[T]):
    status: Optional[int] = Field(default=200)
    code: Optional[int] = Field(default=20000)
    data: T
