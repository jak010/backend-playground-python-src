from src.app.usecase.exceptions.abstract import UseCaseException


class AlreadyExistEmail(UseCaseException):
    """ 이미 존재하는 Eamil """


class AlreadyJoinedMember(UseCaseException):
    """ 이미 가입 처리된 회원 """


class DoesNotExistMember(Exception):
    """ Member를 찾을 수 없음 """


class DeactivateMember(Exception):
    """ 비활성화된 Member """


class MemberCategoryDuplicate(Exception):
    """ Member Category 중복 """
