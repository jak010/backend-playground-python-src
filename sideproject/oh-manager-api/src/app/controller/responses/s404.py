from fastapi import HTTPException
from fastapi.responses import JSONResponse


class NotFound(JSONResponse):
    STATUS_CODE = 404
    CODE = 40400
    ERROR_MESSAGE: str

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


class DoesNotExsitVerification(NotFound):
    ERROR_MESSAGE = "DOES NOT EXIST VERIFICATION "


class DoesNotExistMember(NotFound):
    ERROR_MESSAGE = "DOES NOT EXIST MEMBER"
