from unittest import TestCase

from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import orm
from config.settings import bootstrapping, url, test_url
from src.entity import CouponEntity, CouponIssueEntity
from src.repository.coupon_issue_repository import CouponIssueRepository


class TestCouponIssueRepository(TestCase):

    def setUp(self) -> None:
        self.test_engine = engine.create_engine(test_url)
        self.test_session = scoped_session(sessionmaker(
            bind=self.test_engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False))
        orm.metadata.create_all(self.test_engine)

        bootstrapping()

    def test_save(self):
        coupon_issue = CouponIssueEntity.new(coupon_id=1, user_id=2)

        repository = CouponIssueRepository(session=self.test_session)
        saved_coupon_issue = repository.save(coupon_issue)

        self.assertEqual(coupon_issue.coupon_id, saved_coupon_issue.coupon_id)

    def tearDown(self):
        self.test_session.close()
        orm.metadata.drop_all(self.test_engine)
