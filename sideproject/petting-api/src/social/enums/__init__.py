from enum import Enum


class SocialInviteRequestStatus(Enum):
    WAIT = "WAIT"
    APPROVAL = "APPROVAL"
    REJECT = "REJECT"
