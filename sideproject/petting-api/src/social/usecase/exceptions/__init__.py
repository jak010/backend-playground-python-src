class NotFoundReceiverMember(Exception):
    """ Receiver를 찾을 수 없음 """


class NotFoundSocial(Exception):
    """ 찾을 수 없는 Social 목록 """


class AlreadySocialApproval(Exception):
    """ Approval 처리된 건 """


class AlreadyRequestInvited(Exception):
    """ 이미 초대요청을 보냄 """


class InvalidSocialInviteRequested(Exception):
    """ 친구요청 상태가 WAIT이 아님 """
