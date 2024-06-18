from fastapi.responses import JSONResponse

from libs.responses import codes


class BadRequestInterface(JSONResponse):
    status_code = 400
    code: codes.BadRequestResponseCode
    message: str = None

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            content=self.body()
        )

    @classmethod
    def body(cls):
        return {
            "status_code": 400,
            "code": cls.code,
            "message": cls.message
        }
