from typing import List

from fastapi.responses import JSONResponse

from src.contrib.errors import AbstractError


class AbstractExceptionResponse(JSONResponse):
    status_code: int
    content: str
    message: str

    def body(self):
        return {
            "status_code": self.status_code,
            "content": self.content,
            "message": self.message
        }


class ResultsResponse(JSONResponse):
    STATUS_CODE = 400

    def __init__(self, errors: List[AbstractError]):
        super().__init__(
            status_code=400,
            content=[{
                "error_code": error.CODE,
                "message": error.MESSAGE
            } for error in errors]
        )
