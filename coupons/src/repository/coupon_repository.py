from coupons.config.settings import db_session


class CouponRepository:

    def __init__(self):
        self.session = db_session()

    def find_by_id(self, coupon_id: int):

        self.session.query()

