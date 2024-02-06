import datetime
from unittest import TestCase

from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import orm
from config.settings import bootstrapping
from config.database import TestDataBaseConnection
from src.entity import CouponIssueEntity
from src.entity.coupon_entity import CouponEntity
from src.exceptions import ErroCode, CouponIssueException
from src.repository.coupon_issue_repository import CouponIssueRepository
from src.repository.coupon_repository import CouponRepository
from src.service.coupon_service import CouPonIssueService


class TestCouPonIssueService(TestCase):

    def setUp(self) -> None:
        self.test_engine = engine.create_engine(TestDataBaseConnection.get_url(), echo=True)
        self.test_session = scoped_session(sessionmaker(
            bind=self.test_engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        ))
        orm.Base.metadata.create_all(self.test_engine)

        self.registry = bootstrapping()

        self.coupon_repository = CouponRepository(self.test_session())
        self.coupon_issue_repository = CouponIssueRepository(self.test_session())

        self.sut = CouPonIssueService()
        self.sut.coupon_repository = self.coupon_repository
        self.sut.coupon_issue_repository = self.coupon_issue_repository

    def test_save_coupon_issue_1(self):
        """ 쿠폰 발급 내역이 존재하면 예외를 반환한다. """

        # given
        coupon_issue = CouponIssueEntity(coupon_id=1, user_id=2)
        coupon_issue = self.coupon_issue_repository.save(coupon_issue_entity=coupon_issue)

        # when & then
        with self.assertRaises(CouponIssueException) as e:
            self.sut.save_coupon_issue(
                coupon_id=coupon_issue.coupon_id,
                user_id=coupon_issue.user_id
            )

    def test_save_coupon_issue_2(self):
        """ 쿠폰 발급 내역이 존재하지 않는다면 쿠폰을 발급한다.. """

        # given
        coupon_id = 1
        user_id = 2

        # when
        coupon_issue = self.sut.save_coupon_issue(coupon_id=coupon_id, user_id=user_id)

        # then
        self.assertEqual(
            bool(self.coupon_issue_repository.find_first_coupon_issue(coupon_id=coupon_issue.coupon_id, user_id=coupon_issue.user_id)),
            True
        )

    def test_issue(self):
        """ 발급 수량, 기한, 중복 발급 문제가 없다면 쿠폰을 발급한다.  """

        # given
        user_id = 1
        coupon = CouponEntity(
            coupon_type=1,
            title="선착순 쿠폰",
            total_quantity=100,
            issued_quantity=0,
            date_issue_start=datetime.datetime.now() - datetime.timedelta(days=1),
            date_issue_end=datetime.datetime.now() + datetime.timedelta(days=1),
        )
        saved_coupon = self.coupon_repository.save(coupon)

        # when
        self.sut.issue(coupon_id=saved_coupon.id, user_id=user_id)

        # then
        coupon = self.coupon_repository.find_by_id(coupon_id=saved_coupon.id)
        self.assertEqual(coupon.issued_quantity, 1)

        coupon_issue = self.coupon_issue_repository.find_first_coupon_issue(
            coupon_id=coupon.id,
            user_id=user_id
        )
        self.assertIsNotNone(coupon_issue)

    def test_issue2(self):
        """ 발급 수량에 문제가 있다면 예외를 반환한다.  """

        # given
        user_id = 1
        coupon = CouponEntity(
            coupon_type=1,
            title="선착순 쿠폰",
            total_quantity=100,
            issued_quantity=100,
            date_issue_start=datetime.datetime.now() - datetime.timedelta(days=1),
            date_issue_end=datetime.datetime.now() + datetime.timedelta(days=1),
        )
        saved_coupon = self.coupon_repository.save(coupon)

        # when

        with self.assertRaises(CouponIssueException) as e:
            self.sut.issue(coupon_id=saved_coupon.id, user_id=user_id)

        self.assertEqual(e.exception.error_code, ErroCode.INVALID_COUPON_ISSUE_QUANTITY.value)

    def test_issue3(self):
        """ 발급 기한에 문제가 있다면 예외를 반환한다.  """

        # given
        user_id = 1
        coupon = CouponEntity(
            coupon_type=1,
            title="선착순 쿠폰",
            total_quantity=100,
            issued_quantity=0,
            date_issue_start=datetime.datetime.now() - datetime.timedelta(days=2),
            date_issue_end=datetime.datetime.now() - datetime.timedelta(days=1),
        )
        saved_coupon = self.coupon_repository.save(coupon)

        # when

        with self.assertRaises(CouponIssueException) as e:
            self.sut.issue(coupon_id=saved_coupon.id, user_id=user_id)

        self.assertEqual(e.exception.error_code, ErroCode.INVALID_COUPON_ISSUE_DATE.value)

    def test_issue4(self):
        """ 중복 발급 검증에 문제가 있다면 예외를 반환한다.  """

        # given
        user_id = 1
        coupon = CouponEntity(
            coupon_type=1,
            title="선착순 쿠폰",
            total_quantity=100,
            issued_quantity=0,
            date_issue_start=datetime.datetime.now() - datetime.timedelta(days=1),
            date_issue_end=datetime.datetime.now() + datetime.timedelta(days=1),
        )
        saved_coupon = self.coupon_repository.save(coupon)

        coupon_issue = CouponIssueEntity(coupon_id=coupon.id, user_id=user_id)
        self.coupon_issue_repository.save(coupon_issue_entity=coupon_issue)

        # when

        with self.assertRaises(CouponIssueException) as e:
            self.sut.issue(coupon_id=saved_coupon.id, user_id=user_id)

        self.assertEqual(e.exception.error_code, ErroCode.DUPLICATE_COUPON_ISSUE.value)

    def test_issue5(self):
        """ 쿠폰이 존재하지 않는다면 예외를 반한환다.  """

        # given
        coupon_id = 1
        user_id = 1

        # when

        with self.assertRaises(CouponIssueException) as e:
            self.sut.issue(coupon_id=coupon_id, user_id=user_id)

        self.assertEqual(e.exception.error_code, ErroCode.COUPON_NOT_EXIST.value)

    def tearDown(self):
        self.test_session.close()
        orm.Base.metadata.drop_all(self.test_engine)
        self.registry.dispose()
