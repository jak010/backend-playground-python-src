import datetime
import json
from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import orm
from config.database import TestDataBaseConnection
from config.settings import bootstrapping
from src.entity.coupon_entity import CouponIssueException, ErroCode, CouponEntity
from src.repository.redis_repository import RedisRepository
from src.service.async_coupon_issue_service import CouponIssueRedisService, AsyncCouponIssueService
from src.utils import CoutponRedisUtils
from src.repository.coupon_repository import CouponRepository

test_engine = engine.create_engine(TestDataBaseConnection.get_url(), echo=True)
test_session = scoped_session(sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
))


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
        result = self.sut.available_total_issue_qunatity(
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
                key=CoutponRedisUtils.get_issue_request_key(coupon_id=coupon_id),
                value=x
            )

        # when
        result = self.sut.available_total_issue_qunatity(
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
        self.repository.sadd(CoutponRedisUtils.get_issue_request_key(coupon_id), user_id)

        # when
        result = self.sut.available_user_issue_quantity(coupon_id=coupon_id, user_id=user_id)
        # then
        self.assertFalse(result)

    def tearDown(self) -> None:
        self.repository.client.flushall()


class TestAsyncCouponIssueService(TestCase):
    redis_repository = RedisRepository()

    def setUp(self) -> None:
        orm.Base.metadata.create_all(test_engine)

        self.registry = bootstrapping()

        self.coupon_repository = CouponRepository(test_session)
        self.sut = AsyncCouponIssueService()

    @patch.object(CouponRepository, 'session', test_session)  # XXX: class의 attribute를 patch하기
    def test_issue_1(self):
        """ 쿠폰 발급 - 쿠폰이 존재하지 않는다면 예외를 반환한다. """

        # given
        coupon_id = 1
        user_id = 1

        # when
        with self.assertRaises(CouponIssueException) as e:
            self.sut.issue(coupon_id=coupon_id, user_id=user_id)

        # then
        self.assertEqual(e.exception.error_code, ErroCode.COUPON_NOT_EXIST.value)

    @patch.object(CouponRepository, 'session', test_session)  # XXX: class의 attribute를 patch하기
    def test_issue_2(self):
        """ 쿠폰 발급 - 발급 가능 수량이 존재하지 않는다면 예외를 반환한다. """

        # given
        coupon_id = 1
        user_id = 1
        coupopn_entity = CouponEntity(
            coupon_type="FIRST_COME_FIRST_SEREVED",
            title="선착순 쿠폰 테스트",
            total_quantity=10,
            issued_quantity=0,
            date_issue_start=datetime.datetime.now() - datetime.timedelta(days=1),
            date_issue_end=datetime.datetime.now() + datetime.timedelta(days=2)
        )

        self.coupon_repository.save(coupopn_entity=coupopn_entity)

        key = CoutponRedisUtils.get_issue_request_key(coupon_id=coupopn_entity.id)

        for total_quantity in range(0, coupopn_entity.total_quantity):
            self.redis_repository.sadd(key=key, value=total_quantity)

        # when
        with self.assertRaises(CouponIssueException) as e:
            self.sut.issue(coupon_id=coupon_id, user_id=user_id)

        # then
        self.assertEqual(e.exception.error_code.value, ErroCode.INVALID_COUPON_ISSUE_QUANTITY.value)

    @patch.object(CouponRepository, 'session', test_session)  # XXX: class의 attribute를 patch하기
    def test_issue_3(self):
        """ 쿠폰 발급 - 이미 발급된 유저라면 예외 """

        # given
        user_id = 1
        coupopn_entity = CouponEntity(
            coupon_type="FIRST_COME_FIRST_SEREVED",
            title="선착순 쿠폰 테스트",
            total_quantity=10,
            issued_quantity=0,
            date_issue_start=datetime.datetime.now() - datetime.timedelta(days=1),
            date_issue_end=datetime.datetime.now() + datetime.timedelta(days=2)
        )

        self.coupon_repository.save(coupopn_entity=coupopn_entity)

        self.redis_repository.sadd(key=CoutponRedisUtils.get_issue_request_key(coupon_id=coupopn_entity.id),
                                   value=user_id)

        # when
        with self.assertRaises(CouponIssueException) as e:
            self.sut.issue(coupon_id=coupopn_entity.id, user_id=user_id)

        # then
        self.assertEqual(ErroCode.DUPLICATE_COUPON_ISSUE.value, e.exception.error_code.value)

    @patch.object(CouponRepository, 'session', test_session)  # XXX: class의 attribute를 patch하기
    def test_issue_4(self):
        """ 쿠폰 발급 - 발급 기한이 유효하지 않다면 예외를 반환한다, """

        # given
        user_id = 1
        coupopn_entity = CouponEntity(
            coupon_type="FIRST_COME_FIRST_SEREVED",
            title="선착순 쿠폰 테스트",
            total_quantity=10,
            issued_quantity=0,
            date_issue_start=datetime.datetime.now() + datetime.timedelta(days=1),
            date_issue_end=datetime.datetime.now() + datetime.timedelta(days=2)
        )

        self.coupon_repository.save(coupopn_entity=coupopn_entity)

        self.redis_repository.sadd(key=CoutponRedisUtils.get_issue_request_key(coupon_id=coupopn_entity.id),
                                   value=user_id)

        # when
        with self.assertRaises(CouponIssueException) as e:
            self.sut.issue(coupon_id=coupopn_entity.id, user_id=user_id)

        # then
        self.assertEqual(ErroCode.INVALID_COUPON_ISSUE_DATE.value, e.exception.error_code.value)

    @patch.object(CouponRepository, 'session', test_session)  # XXX: class의 attribute를 patch하기
    def test_issue_5(self):
        """ 쿠폰 발급 - 쿠폰 발급을 기록한다. """

        # given
        coupon_id = 1
        user_id = 1
        coupopn_entity = CouponEntity(
            coupon_type="FIRST_COME_FIRST_SEREVED",
            title="선착순 쿠폰 테스트",
            total_quantity=10,
            issued_quantity=0,
            date_issue_start=datetime.datetime.now() - datetime.timedelta(days=1),
            date_issue_end=datetime.datetime.now() + datetime.timedelta(days=2)
        )

        self.coupon_repository.save(coupopn_entity=coupopn_entity)
        cache_key = CoutponRedisUtils.get_issue_request_key(coupon_id=coupon_id)

        # when
        self.sut.issue(coupon_id=coupopn_entity.id, user_id=user_id)

        # then
        is_saved = self.redis_repository.sismember(
            key=cache_key,
            value=user_id
        )

        self.assertTrue(is_saved)

    @patch.object(CouponRepository, 'session', test_session)  # XXX: class의 attribute를 patch하기
    def test_issue_6(self):
        """ 쿠폰 발급 - 발급 요청이 성공하면 쿠폰 발급 후에 적재된다.. """

        # given
        coupon_id = 1
        user_id = 1
        coupopn_entity = CouponEntity(
            coupon_type="FIRST_COME_FIRST_SEREVED",
            title="선착순 쿠폰 테스트",
            total_quantity=10,
            issued_quantity=0,
            date_issue_start=datetime.datetime.now() - datetime.timedelta(days=1),
            date_issue_end=datetime.datetime.now() + datetime.timedelta(days=2)
        )

        self.coupon_repository.save(coupopn_entity=coupopn_entity)

        # when
        self.sut.issue(coupon_id=coupopn_entity.id, user_id=user_id)

        # then
        saved_issue_request = self.redis_repository.lpop(key=CoutponRedisUtils.get_issue_request_queue_key())
        data = json.loads(saved_issue_request.decode())

        self.assertEqual(coupon_id, data['coupon_id'])

    def tearDown(self) -> None:
        self.redis_repository.client.flushall()

        test_session.close()
        orm.Base.metadata.drop_all(test_engine)
        self.registry.dispose()
