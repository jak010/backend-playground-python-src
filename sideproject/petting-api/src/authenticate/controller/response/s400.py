from libs.responses import codes
from libs.responses.s400 import BadRequestInterface


class KaKaoAuthenticateFailureResponse(BadRequestInterface):
    message = "Authenticate Faile, KaKao"
    code = codes.BadRequestResponseCode.KAKAO_LOGIN_FAILURE.value
