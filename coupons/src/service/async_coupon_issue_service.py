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


class AsyncCouponIssueService:

    def __init__(self):
        self.repository = RedisRepository()
        self.coupon_issue_redis_serivce = CouponIssueRedisService()
        self.coupon_issue_service = CouPonIssueService()

        self.coupon_cache_service = CouPonCacheServce()

        self.coupon_repository = CouponRepository()

    def issue(self, coupon_id, user_id):
        coupon: CouponRedisEntity = self.coupon_cache_service.get_coupon_cache(coupon_id=coupon_id)
        coupon.check_issuable_coupon()

        # Redis Distribute Lock
        # XXX: RPS 800 ~ 900 사이 밖에 안나옴
        with DistributeLockExecutor(name=f"coupon_{coupon_id}", redis_client=redis_client(), expire=60, auto_renewal=True):
            self.coupon_issue_redis_serivce.check_coupon_issue_quantitiy(
                coupon_redis_entity=coupon,
                user_id=user_id
            )

            self.issue_request(coupon_id=coupon.id, user_id=user_id)

    def issue_request(self, coupon_id, user_id):
        issue_reuqest = CouponIssueRequestDto(coupon_id=coupon_id, user_id=user_id)

        self.repository.client.sadd(CouponRedisUtils.get_issue_request_key(coupon_id), user_id)
        self.repository.rpush(
            CouponRedisUtils.get_issue_request_queue_key(),
            json.dumps(issue_reuqest.to_dict())
        )  # 쿠폰 발급 대기열 큐
