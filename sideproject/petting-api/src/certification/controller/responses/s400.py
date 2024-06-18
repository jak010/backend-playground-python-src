from libs.responses import codes
from libs.responses.s400 import BadRequestInterface


class AlredaySmsCerificationRequestResponse(BadRequestInterface):
    message = "Alreday SMS Code Request"
    code = codes.BadRequestResponseCode.SMS_CERTIFICATION_REQUEST.value


class AlredaySmsCerificationCeompleteResponse(BadRequestInterface):
    message = "Alreday SMS Certification Complete"
    code = codes.BadRequestResponseCode.SMS_CERTIFICATION_ALREADY_COMPLETE.value
