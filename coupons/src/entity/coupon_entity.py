import datetime
from typing import Optional

from pydantic import dataclasses
from enum import Enum


class ErroCode(Enum):
    INVALID_COUPON_ISSUE_QUANTITY = 1
    INVALID_COUPON_ISSUE_DATE = 2


class CouponException(Exception):
    """ CouponException """


class CouponIssueException(CouponException):
    """ Coupon Issue Exception"""

    def __init__(self, error_code: int, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(error_code, message)

    def __str__(self):
        return f"{self.error_code},{self.message}"


@dataclasses.dataclass
class CouponEntity:
    id: int = dataclasses.Field(default=None)
    title: str = dataclasses.Field(default=None)
    coupon_types: str = dataclasses.Field(default=None)
    total_quantity: Optional[int] = dataclasses.Field(default=None)
    issued_quantity: int = dataclasses.Field(default=None)
    discount_amount: int = dataclasses.Field(default=None)
    min_available_amount: int = dataclasses.Field(default=None)
    date_issue_start: datetime.datetime = dataclasses.Field(default=None)
    date_issue_end: datetime.datetime = dataclasses.Field(default=None)
    date_created: datetime.datetime = dataclasses.Field(default=datetime.datetime.now())
    date_updated: datetime.datetime = dataclasses.Field(default=datetime.datetime.now())

    def avaliable_issue_quantitiy(self) -> bool:
        """ 발급 수량 검증 """
        if self.total_quantity is None:
            return True
        return self.total_quantity > self.issued_quantity

    def avaliable_issue_date(self):
        """ 쿠폰 발급 기간 검증 """
        import datetime
        now = datetime.datetime.now()
        return self.date_issue_start < now < self.date_issue_end

    def issue(self):
        if not self.avaliable_issue_quantitiy():
            raise CouponIssueException(
                ErroCode.INVALID_COUPON_ISSUE_QUANTITY.value, message=f"발급 가능한 수량 초과 total:{self.total_quantity},issued:{self.issued_quantity}")
        if not self.avaliable_issue_date():
            raise CouponIssueException(
                ErroCode.INVALID_COUPON_ISSUE_DATE.value,
                message=f"발급 가능한 일자가 아님. request:{self.date_created}, issue_start:{self.date_issue_start} issue_end:{self.date_issue_end}")

        self.issued_quantity += 1
