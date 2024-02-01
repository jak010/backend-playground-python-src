from unittest import TestCase

from coupons.src.entity.coupon_issue_entity import CouponIssueEntity


class TestCouPonIssueService(TestCase):

    def test(self):
        """ 쿠폰 발급 내역이 존재하면 예외를 반환한다. """
        coupon_issue = CouponIssueEntity(coupon_id=1, user_id=1)

    def test_issue(self):
        self.fail()

    def test_find_coupon(self):
        self.fail()

    def test_save_coupon_issue(self):
        self.fail()

    def test__check_already_issuance(self):
        self.fail()
