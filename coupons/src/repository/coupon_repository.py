from sqlalchemy import exc
from sqlalchemy.orm import Session

from src.entity.coupon_entity import CouponEntity, CouponIssueException, ErroCode


class CouponRepository:

    def __init__(self, session=None):
        self.session: Session = session

    def find_by_id(self, coupon_id: int) -> CouponEntity:
        query = self.session.query(CouponEntity).filter(CouponEntity.id == coupon_id)
        query = query.one_or_none()

        if query is not None:
            return query
        raise Exception("Coupon Does Not Exist")

    def save(self, coupopn_entity: CouponEntity):
        try:
            self.session.add(coupopn_entity)
            self.session.flush()
        except exc.IntegrityError as e:
            raise CouponIssueException(
                ErroCode.DUPLICATE_COUPON_ISSUE,
                message=f"중복"
            )
        return coupopn_entity
