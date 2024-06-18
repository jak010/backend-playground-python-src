from libs.responses import codes
from libs.responses.s400 import BadRequestInterface


class PetRegisterLimitExceededResponse(BadRequestInterface):
    message = "Pet Register Limit Exceeded "
    code = codes.BadRequestResponseCode.PET_REGISTERD_LIMIT_EXCEEDED.value


class PetRegisterDuplicateResponse(BadRequestInterface):
    message = "DULPLICATE PET"
    code = codes.BadRequestResponseCode.PET_REGISTERD_DUPLICATE.value


class PatAttachmnetDuplicateResponse(BadRequestInterface):
    message = "DULPLICATE PET ATTACHMNET"
    code = codes.BadRequestResponseCode.PET_ATTAACHMENT_REGISTERD_DUPLICATE.value


class PetAttachmentMaxUploadLimitResponse(BadRequestInterface):
    message = "LIMIT, PET ATTACHMENT"
    code = codes.BadRequestResponseCode.PET_ATTAACHMENT_REGISTERD_LIMIT_DUPLICATE.value


class PetAttachmentFileAlreadySetPrimaryResponse(BadRequestInterface):
    message = "LIMIT, PET ATTACHMENT Already Primary Setup"
    code = codes.BadRequestResponseCode.PET_ATTAACHMENT_REGISTERD_ALREADY_PIMART_SET.value
