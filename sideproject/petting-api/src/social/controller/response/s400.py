from libs.responses import codes
from libs.responses.s400 import BadRequestInterface


class InvalidReceiverMember(BadRequestInterface):
    message = "INVALID, RECEIVER MEMBER"
    code = codes.BadRequestResponseCode.SOCIAL_INVALIDE_RECEIVER_MEMBER.value


class AlreadyRequestInvited(BadRequestInterface):
    message = "INVALID, Already Social Request Invited"
    code = codes.BadRequestResponseCode.SOCIAL_ALREADY_INVITED_REQUEST.value


class AlreadySocialApproval(BadRequestInterface):
    message = "INVALID, Already Social Request Approval"
    code = codes.BadRequestResponseCode.SOCIAL_ALREADY_APPROVAL_REQUEST.value


class InvalidSocialInvitedRequest(BadRequestInterface):
    message = "INVALID, SOCIAL STATUS"
    code = codes.BadRequestResponseCode.SOCIAL_ALREADY_INVITED_REQUEST.value
