from fastapi.responses import JSONResponse

from libs.responses import codes


class NotFoundInterface(JSONResponse):
    status_code = 404
    code: codes.NotFoundResponseCode
    message: str = None

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            content=self.body()
        )

    @classmethod
    def body(cls):
        return {
            "status_code": 404,
            "code": cls.code,
            "message": cls.message
        }
