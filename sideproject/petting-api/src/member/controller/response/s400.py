from libs.responses import codes
from libs.responses.s400 import BadRequestInterface


class MemberDuplicateResponse(BadRequestInterface):
    message = "DUPLICATE, MEMBER"
    code = codes.BadRequestResponseCode.MEMBER_DUPLICATE_ERROR.value
