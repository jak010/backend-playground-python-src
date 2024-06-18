from fastapi import HTTPException
from fastapi.responses import JSONResponse


class UnAuthorized(JSONResponse):
    STATUS_CODE = 401
    CODE = 40100
    ERROR_MESSAGE: str = "UnAuthorized"

    def __init__(self):
        super().__init__(
            status_code=self.STATUS_CODE,
            content={
                "message": self.ERROR_MESSAGE
            }
        )

    @classmethod
    def get_data(cls):
        return {
            "status": cls.STATUS_CODE,
            "code": cls.CODE,
            "message": cls.ERROR_MESSAGE
        }
