from fastapi import HTTPException
from fastapi.responses import JSONResponse


class BadRequest(JSONResponse):
    STATUS_CODE = 400
    CODE = 40000
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


class AlreadyExistEmail(BadRequest):
    CODE = 40100
    ERROR_MESSAGE = "The email is already in use. Please use a different email."


class AlreadyJoinedMember(BadRequest):
    CODE = 40101
    ERROR_MESSAGE = "This Member Already Join in Platform"


class InvalidEmail(BadRequest):
    CODE = 40150
    ERROR_MESSAGE = "This email is invalid"


class InvalidAudition(BadRequest):
    CODE = 40151
    ERROR_MESSAGE = "This auditions is invalid"


class VerificationCodeExpired(BadRequest):
    CODE = 40201
    ERROR_MESSAGE = "The verification code has been invalidated and is therefore unusable."


class VerificationCodeIsNotPending(BadRequest):
    CODE = 40201
    ERROR_MESSAGE = "The verification code has been used."


class DeactivateMember(BadRequest):
    CODE = 40301
    ERROR_MESSAGE = "Deactivate Member"


class DuplicateMemberCategory(BadRequest):
    CODE = 40302
    ERROR_MESSAGE = "Duplicate Member Category"


class SubmissionFailure(BadRequest):
    CODE = 40303
    ERROR_MESSAGE = "SubmissionFailure"
