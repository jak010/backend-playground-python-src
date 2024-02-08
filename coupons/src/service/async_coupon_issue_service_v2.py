import json

from redis_lock import Lock as DistributeLockExecutor

from config.settings import redis_client
from src.entity.coupon_redis_entity import CouponRedisEntity
from src.repository.coupon_repository import CouponRepository
from src.repository.redis_repository import CouponIssueRequestDto, RedisRepository
from src.service.coupon_cache_service import CouPonCacheServce
from src.service.coupon_issue_redis_service import CouponIssueRedisService
from src.service.coupon_issue_service import CouPonIssueService
from src.utils import CouponRedisUtils


class AsyncCouponIssueServiceV2:

    def __init__(self):
        self.repository = RedisRepository()
        self.coupon_issue_redis_serivce = CouponIssueRedisService()
        self.coupon_issue_service = CouPonIssueService()

        self.coupon_cache_service = CouPonCacheServce()

        self.coupon_repository = CouponRepository()

    def issue(self, coupon_id, user_id):
        coupon: CouponRedisEntity = self.coupon_cache_service.get_coupon_cache(coupon_id=coupon_id)
        coupon.check_issuable_coupon()
        self.issue_request(coupon_id=coupon.id, user_id=user_id, total_issue_quantity=coupon.total_quantity)

    def issue_request(self, coupon_id, user_id, total_issue_quantity):
        if total_issue_quantity is None:
            self.repository.issu_request(coupon_id, user_id, 99999)

        self.repository.issu_request(coupon_id, user_id, total_issue_quantity)
