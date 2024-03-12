import datetime
from typing import Optional

# from pydantic import dataclasses
import dataclasses

from src.exceptions import ErroCode, CouponIssueException


@dataclasses.dataclass
class CouponEntity:
    id: int = dataclasses.field(default=None)
    title: str = dataclasses.field(default=None)
    coupon_type: str = dataclasses.field(default=None)
    total_quantity: Optional[int] = dataclasses.field(default=None)
    issued_quantity: int = dataclasses.field(default=None)
    discount_amount: int = dataclasses.field(default=0)
    min_available_amount: int = dataclasses.field(default=0)
    date_issue_start: datetime.datetime = dataclasses.field(default=None)
    date_issue_end: datetime.datetime = dataclasses.field(default=None)
    date_created: datetime.datetime = dataclasses.field(default=datetime.datetime.now())
    date_updated: datetime.datetime = dataclasses.field(default=datetime.datetime.now())

    def avaliable_issue_quantitiy(self) -> bool:
        """ 발급 수량 검증 """
        if self.total_quantity is None:
            return True
        return self.total_quantity > self.issued_quantity

    def avaliable_issue_date(self):
        """ 쿠폰 발급 기간 검증 """
        import datetime
        now = datetime.datetime.now()
        return self.date_issue_start <= now <= self.date_issue_end

    def issue(self):
        if not self.avaliable_issue_quantitiy():
            raise CouponIssueException(
                ErroCode.INVALID_COUPON_ISSUE_QUANTITY.value, message=f"발급 가능한 수량 초과 total:{self.total_quantity},issued:{self.issued_quantity}")
        if not self.avaliable_issue_date():
            raise CouponIssueException(
                ErroCode.INVALID_COUPON_ISSUE_DATE.value,
                message=f"발급 가능한 일자가 아님. request:{self.date_created}, issue_start:{self.date_issue_start} issue_end:{self.date_issue_end}")

        self.issued_quantity += 1

    def to_dict(self):
        return dataclasses.asdict(self)
