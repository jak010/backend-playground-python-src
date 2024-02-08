from unittest import TestCase
from unittest.mock import Mock, call, MagicMock

from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import orm
from src.exceptions import CouponIssueException
from config.database import TestDataBaseConnection
from config.settings import bootstrapping
from src.repository.coupon_repository import CouponRepository
from src.repository.redis_repository import RedisRepository
from src.service.async_coupon_issue_service_v2 import AsyncCouponIssueServiceV2
from src.consumer.coupon_issue_listener import CouponIssueListener
from src.service.coupon_issue_service import CouPonIssueService

test_engine = engine.create_engine(TestDataBaseConnection.get_url(), echo=True)
test_session = scoped_session(sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
))


class TestCouponIssueListener(TestCase):
    redis_repository = RedisRepository()
    coupon_issue_service = CouPonIssueService()

    def setUp(self) -> None:
        orm.Base.metadata.create_all(test_engine)

        self.registry = bootstrapping()

        self.sut = CouponIssueListener()

    def test_issue(self):
        """ 쿠폰 발급 큐에 처리 대상이 없다면 발급을 하지 않는다. """

        # given
        mock_coupon_issue_service = Mock()
        self.sut.coupon_issue_service = mock_coupon_issue_service

        # when
        self.sut.issue()

        # then
        mock_coupon_issue_service.issue.assert_not_called()

    def test_issue2(self):
        """ 쿠폰 발급 큐에 처리 대상이 없다면 발급한다."""

        # given
        coupon_id = 1
        user_id = 1
        total_quantity = 999
        self.redis_repository.issu_request(coupon_id=coupon_id, user_id=user_id, total_issue_quantity=total_quantity)

        mock_coupon_issue_service = Mock()
        self.sut.coupon_issue_service = mock_coupon_issue_service

        # when
        self.sut.issue()

        # then
        mock_coupon_issue_service.issue.assert_called()

    def test_issue3(self):
        """ 쿠폰 발급 요청 순서 검증"""

        # given
        coupon_id = 1
        user_id1 = 1
        user_id2 = 2
        user_id3 = 3
        total_quantity = 999
        self.redis_repository.issu_request(coupon_id=coupon_id, user_id=user_id1, total_issue_quantity=total_quantity)
        self.redis_repository.issu_request(coupon_id=coupon_id, user_id=user_id2, total_issue_quantity=total_quantity)
        self.redis_repository.issu_request(coupon_id=coupon_id, user_id=user_id3, total_issue_quantity=total_quantity)

        mock_coupon_issue_service = MagicMock(spec=CouPonIssueService)
        mock_coupon_issue_service.issue.return_value = [call(coupon_id=coupon_id, user_id=user_id1), call(coupon_id=coupon_id, user_id=user_id2),
                                                        call(coupon_id=coupon_id, user_id=user_id3)]
        #
        self.sut.coupon_issue_service = mock_coupon_issue_service

        # when
        self.sut.issue()

        # then
        calls = [call(coupon_id=coupon_id, user_id=user_id1), call(coupon_id=coupon_id, user_id=user_id2), call(coupon_id=coupon_id, user_id=user_id3)]

        mock_coupon_issue_service.issue.assert_has_calls(calls=calls)

        # self.assertEqual(result, expected)
        #
        # mock_coupon_issue_service.issue.assert_called_once_with(coupon_id=coupon_id, total_quantity=total_quantity)

    def tearDown(self) -> None:
        self.redis_repository.client.flushall()

        test_session.close()
        orm.Base.metadata.drop_all(test_engine)
        self.registry.dispose()
