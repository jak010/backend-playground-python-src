from libs.responses import codes
from libs.responses.s404 import NotFoundInterface


class NotFoundSmsCerificationCode(NotFoundInterface):
    message = "Not Exist Cerification Code"
    code = codes.NotFoundResponseCode.SMS_CERTIFICATION.value
