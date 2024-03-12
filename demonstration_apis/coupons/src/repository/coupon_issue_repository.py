from src.entity.coupon_issue_entity import CouponIssueEntity
from typing import Optional
from fastapi import Depends
from config.settings import db_session

from sqlalchemy.orm import Session
from sqlalchemy import exc
from src.entity.coupon_entity import CouponEntity
from src.exceptions import ErroCode, CouponIssueException

from config.settings import db_session
from functools import cached_property


class CouponIssueRepository:

    def __init__(self, session: Session = db_session):
        self._session: Session = session

    @cached_property
    def session(self):
        return self._session

    def save(self, coupon_issue_entity: CouponIssueEntity):

        try:
            self.session.add(coupon_issue_entity)
        except exc.IntegrityError as e:
            raise CouponIssueException(
                ErroCode.DUPLICATE_COUPON_ISSUE.value,
                message=f"중복"
            )
        except Exception as e:
            raise e

        return coupon_issue_entity

    def find_first_coupon_issue(self, coupon_id: int, user_id: int) -> Optional[CouponIssueEntity]:
        return self.session.query(CouponIssueEntity) \
            .filter(CouponIssueEntity.coupon_id == coupon_id) \
            .filter(CouponIssueEntity.user_id == user_id) \
            .one_or_none()
