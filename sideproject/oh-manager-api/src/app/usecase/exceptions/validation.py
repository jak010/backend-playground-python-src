from src.app.usecase.exceptions.abstract import UseCaseException


class InvalidEmail(UseCaseException):
    """ 유효하지 않은 Email 형식 """


class InvalidCredential(UseCaseException):
    """ 인증 정보가 유효하지 않음 """


class InvalidSubmissions(UseCaseException):
    """ 유효하지 않은 신청 """


class InvalidAuditions(UseCaseException):
    """ 유효하지 않은 오디션 정보 """
