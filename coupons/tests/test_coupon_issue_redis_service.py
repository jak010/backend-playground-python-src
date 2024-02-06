from unittest import TestCase

from src.repository.redis_repository import RedisRepository
from src.service.coupon_issue_redis_service import CouponIssueRedisService
from src.utils import CouponRedisUtils


class TestCouponIssueRedisService(TestCase):
    sut = CouponIssueRedisService()

    def setUp(self) -> None:
        self.repository = RedisRepository()

    def test_available_total_quantity(self):
        """ 쿠폰 수량 검증 - 발급 가능한 수량이 존재하면 true를 반환한다. """

        # given
        total_issue_quantity = 10
        user_id = 1

        # when
        result = self.sut.available_total_issue_quantity(
            total_issue_quantity,
            user_id
        )

        # then
        self.assertTrue(result)

    def test_available_total_quantity2(self):
        """ 쿠폰 수량 검증 - 발급 가능한 수량이 모두 소진되면  false를 반환한다.. """

        # given
        total_issue_quantity = 10
        coupon_id = 1

        for x in range(total_issue_quantity):
            self.repository.sadd(
                key=CouponRedisUtils.get_issue_request_key(coupon_id=coupon_id),
                value=x
            )

        # when
        result = self.sut.available_total_issue_quantity(
            total_issue_quantity,
            coupon_id
        )

        # then
        self.assertFalse(result)

    def test_available_user_issue_quantity1(self):
        """ 쿠폰 중복 발급 검증 - 발급된 내역에 유저가 존재하지 않으면 true를 반환한다. """
        # given
        coupon_id = 1
        user_id = 1

        # when
        result = self.sut.available_user_issue_quantity(coupon_id=coupon_id, user_id=user_id)
        # then
        self.assertTrue(result)

    def test_available_user_issue_quantity2(self):
        """ 쿠폰 중복 발급 검증 - 발급된 내역에 유저가 존재하지 않으면 false를 반환한다. """
        # given
        coupon_id = 1
        user_id = 1
        self.repository.sadd(CouponRedisUtils.get_issue_request_key(coupon_id), user_id)

        # when
        result = self.sut.available_user_issue_quantity(coupon_id=coupon_id, user_id=user_id)
        # then
        self.assertFalse(result)

    def tearDown(self) -> None:
        self.repository.client.flushall()
