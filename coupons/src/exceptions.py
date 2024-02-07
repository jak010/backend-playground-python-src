from enum import Enum


class ErroCode(Enum):
    INVALID_COUPON_ISSUE_QUANTITY = 1
    INVALID_COUPON_ISSUE_DATE = 2
    COUPON_NOT_EXIST = 3

    DUPLICATE_COUPON_ISSUE = 4

    FIND_COUPON_ISSUE_REQUEST = 5


class CouponException(Exception):
    """ CouponException """


class CouponDoesNotExist(CouponException):
    """ Find Not Coupon """


class CouponIssueException(CouponException):
    """ Coupon Issue Exception"""

    def __init__(self, error_code: int, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(error_code, message)

    def __str__(self):
        return f"{self.error_code},{self.message}"
