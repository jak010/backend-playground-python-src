from src.entity.coupon_issue_entity import CouponIssueEntity
from typing import Optional

from config.settings import db_session

from sqlalchemy.orm import Session
from sqlalchemy import exc
from src.entity.coupon_entity import CouponEntity, CouponIssueException, ErroCode


class CouponIssueRepository:

    def __init__(self, session=None):
        self.session: Session = session

    def save(self, coupon_issue_entity: CouponIssueEntity):

        try:
            self.session.add(coupon_issue_entity)
            self.session.flush()

        except exc.IntegrityError as e:
            raise CouponIssueException(
                ErroCode.DUPLICATE_COUPON_ISSUE.value,
                message=f"중복"
            )

        return coupon_issue_entity

    def find_first_coupon_issue(self, coupon_id: int, user_id: int) -> Optional[CouponIssueEntity]:
        return self.session.query(CouponIssueEntity) \
            .filter(CouponIssueEntity.coupon_id == coupon_id) \
            .filter(CouponIssueEntity.user_id == user_id)\
            .one_or_none()
