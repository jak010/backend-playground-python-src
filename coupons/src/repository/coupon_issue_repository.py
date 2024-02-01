from coupons.src.entity.coupon_issue_entity import CouponIssueEntity
from typing import Optional


class CouponIssueRepository:

    def __init__(self):
        self.session = None

    def save(self, coupon_issue_entity: CouponIssueEntity):
        return True

    def find_first_coupon_issue(self, coupon_id: int, user_id: int) -> Optional[CouponIssueEntity]:
        return True
