import datetime
import unittest

from coupons.src.entity.coupon_entity import CouponEntity
from src.exceptions import ErroCode, CouponIssueException


class TestCouponEntity(unittest.TestCase):

    def test(self):
        coupon = CouponEntity(total_quantity=100, issued_quantity=99)
        self.assertTrue(coupon)

    def test_avaliable_issue_quantitiy2(self):
        """ 발급 수량이 소진되었다면 false를 반환한다. """
        coupon = CouponEntity(total_quantity=100, issued_quantity=100)
        self.assertFalse(coupon.avaliable_issue_quantitiy())

    def test_avaliable_issue_quantitiy3(self):
        """ 발급 수량이 설정되지 않았다면 true를 반환한다. """
        coupon = CouponEntity(total_quantity=None, issued_quantity=100)
        self.assertTrue(coupon.avaliable_issue_quantitiy())

    def test_avaliable_issue_date(self):
        """ 발급 기간이 시작되지 않음 """
        from datetime import timedelta
        coupon = CouponEntity(
            date_issue_start=datetime.datetime.now() + timedelta(days=1),
            date_issue_end=datetime.datetime.now() + timedelta(days=2),
        )

        self.assertFalse(coupon.avaliable_issue_date())

    def test_avaliable_issue_date2(self):
        """ 발급 기간에 해당됨 """
        from datetime import timedelta
        coupon = CouponEntity(
            date_issue_start=datetime.datetime.now() - timedelta(days=1),
            date_issue_end=datetime.datetime.now() + timedelta(days=2),
        )

        self.assertTrue(coupon.avaliable_issue_date())

    def test_avaliable_issue_date3(self):
        """ 발급 기간이 종료됨 """
        from datetime import timedelta
        coupon = CouponEntity(
            date_issue_start=datetime.datetime.now() - timedelta(days=2),
            date_issue_end=datetime.datetime.now() - timedelta(days=1),
        )

        self.assertFalse(coupon.avaliable_issue_date())

    def test_issue1(self):
        """ 발급기간이 유효하다면 발급에 성공한다. """
        from datetime import timedelta
        coupon = CouponEntity(
            total_quantity=100,
            issued_quantity=99,
            date_issue_start=datetime.datetime.now() - timedelta(days=1),
            date_issue_end=datetime.datetime.now() + timedelta(days=1),
        )
        coupon.issue()

        self.assertEqual(coupon.issued_quantity, 100)

    def test_issue2(self):
        """ 발급 수량이 초과하면 예외를 반환한다. """
        from datetime import timedelta
        coupon = CouponEntity(
            total_quantity=100,
            issued_quantity=100,
            date_issue_start=datetime.datetime.now() - timedelta(days=1),
            date_issue_end=datetime.datetime.now() + timedelta(days=1),
        )

        with self.assertRaises(CouponIssueException) as e:
            coupon.issue()

        self.assertEqual(e.exception.error_code, ErroCode.INVALID_COUPON_ISSUE_QUANTITY.value)

    def test_issue3(self):
        """ 발급기간이 유효하지 않으면 예외를 반환한다.. """
        from datetime import timedelta
        coupon = CouponEntity(
            total_quantity=100,
            issued_quantity=99,
            date_issue_start=datetime.datetime.now() + timedelta(days=1),
            date_issue_end=datetime.datetime.now() + timedelta(days=2)
        )

        with self.assertRaises(CouponIssueException) as e:
            coupon.issue()

        self.assertEqual(e.exception.error_code, ErroCode.INVALID_COUPON_ISSUE_DATE.value)
