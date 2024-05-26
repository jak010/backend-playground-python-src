from fastapi.responses import JSONResponse


class BaseErrorResponse(JSONResponse):
    STATUS_CODE: int = None
    ERROR_CODE: int = None
    MESSAGE: str = None

    def __init__(self):
        super().__init__(
            status_code=self.STATUS_CODE,
            content=self.body()
        )

    @classmethod
    def body(cls):
        return {
            "status_code": cls.STATUS_CODE,
            "error_code": cls.ERROR_CODE,
            "message": cls.MESSAGE
        }


class BadRequest(BaseErrorResponse):
    STATUS_CODE = 400
    ERROR_CODE = 400_000
    MESSAGE = ""


class UnAuthorized(BaseErrorResponse):
    STATUS_CODE = 401
    ERROR_CODE = 401_000
    MESSAGE = ""


class Forbidden(BaseErrorResponse):
    STATUS_CODE = 403
    ERROR_CODE = 403_000
    MESSAGE = ""


class NotFound(BaseErrorResponse):
    STATUS_CODE = 404
    ERROR_CODE = 404_000
    MESSAGE = ""
