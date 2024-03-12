import datetime
import dataclasses


@dataclasses.dataclass(unsafe_hash=True)
class CouponIssueEntity:
    id: int = dataclasses.field(init=False)
    coupon_id: int = dataclasses.field(default=None)
    user_id: int = dataclasses.field(default=None)
    date_issued: datetime.datetime = dataclasses.field(default=datetime.datetime.now())
    date_used: datetime.datetime = dataclasses.field(default=None)
    date_created: datetime.datetime = dataclasses.field(default=datetime.datetime.now())
    date_updated: datetime.datetime = dataclasses.field(default=datetime.datetime.now())

    @classmethod
    def new(
            cls,
            *,
            coupon_id: int,
            user_id: int,
            date_used: datetime.datetime = None
    ):
        return cls(
            coupon_id=coupon_id,
            user_id=user_id,
            date_issued=datetime.datetime.now(),
            date_used=date_used,
            date_created=datetime.datetime.now(),
            date_updated=datetime.datetime.now()
        )
