from src.app.usecase.exceptions.abstract import UseCaseException


class VerificationCodeExpired(UseCaseException):
    """ 인증 코드 유효기간 만료 """


class VerificationCodeIsNotPending(UseCaseException):
    """ 인증 코드가 검증할 수 있는 상태가 아님 """


class DoesNotExistVerification(UseCaseException):
    """ 인증내역을 찾을 수 없음 """

