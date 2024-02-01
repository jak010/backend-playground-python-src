import datetime

from pydantic import dataclasses


@dataclasses.dataclass
class CouponIssueEntity:
    id: int = dataclasses.Field(default=None)
    coupon_id: int = dataclasses.Field(default=None)
    user_id: int = dataclasses.Field(default=None)
    date_issued: datetime.datetime = dataclasses.Field(default=None)
    date_used: datetime.datetime = dataclasses.Field(default=None)
    date_created: datetime.datetime = dataclasses.Field(default=None)
    date_updated: datetime.datetime = dataclasses.Field(default=None)
