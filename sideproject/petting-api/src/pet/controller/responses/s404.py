from libs.responses import codes
from libs.responses.s404 import NotFoundInterface


class NotFoundPetResponse(NotFoundInterface):
    message = "Not Found, PET"
    code = codes.NotFoundResponseCode.DOES_NOT_EXIST_PET.value
