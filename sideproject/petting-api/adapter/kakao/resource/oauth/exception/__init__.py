
class KaKaoTokenException(Exception):
    """ KaKao Token API Exception """


class KaKaoAccessTokenIssuedFail(KaKaoTokenException):
    """ KaKao, 토큰 발급에 실패함 """