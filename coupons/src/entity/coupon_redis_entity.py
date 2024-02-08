from __future__ import annotations

import dataclasses
import datetime
import json

from src.entity.coupon_entity import CouponEntity
from src.exceptions import CouponIssueException, ErroCode


@dataclasses.dataclass
class CouponRedisEntity:
    id: int
    coupon_type: str
    total_quantity: int

    available_issue_quantity: bool

    date_issue_start: datetime.datetime
    date_issue_end: datetime.datetime

    @classmethod
    def of(cls, coupon: CouponEntity) -> CouponRedisEntity:
        return cls(
            id=coupon.id,
            coupon_type=coupon.coupon_type,
            total_quantity=coupon.total_quantity,
            available_issue_quantity=coupon.avaliable_issue_quantitiy(),
            date_issue_start=coupon.date_issue_start,
            date_issue_end=coupon.date_issue_end
        )

    def available_issue_date(self) -> bool:
        now = datetime.datetime.now()

        if isinstance(self.date_issue_start, str):
            self.date_issue_start = datetime.datetime.strptime(self.date_issue_start, "%Y-%m-%dT%H:%M:%S")
        if isinstance(self.date_issue_end, str):
            self.date_issue_end = datetime.datetime.strptime(self.date_issue_end, "%Y-%m-%dT%H:%M:%S")

        return self.date_issue_start < now < self.date_issue_end

    def check_issuable_coupon(self):
        if not self.available_issue_quantity:
            raise CouponIssueException(
                ErroCode.INVALID_COUPON_ISSUE_QUANTITY,
                f"모든 발급 수량이 소진되었습니다. coupon_id : {self.id}"
            )

        if not self.available_issue_date():
            raise CouponIssueException(
                ErroCode.INVALID_COUPON_ISSUE_DATE,
                f"발급 가능한 일자가 아닙니3다. request : {datetime.datetime.now()}, issueStart: {self.date_issue_start}, issueEnd: {self.date_issue_end}"
            )

    def to_json(self) -> dict:
        return json.dumps({
            'id': self.id,
            'coupon_type': self.coupon_type,
            'total_quantity': self.total_quantity,
            'available_issue_quantity': self.available_issue_quantity,
            'date_issue_start': self.date_issue_start.isoformat(),
            'date_issue_end': self.date_issue_end.isoformat()
        }, indent=4)
