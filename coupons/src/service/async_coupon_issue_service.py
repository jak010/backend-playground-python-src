import json

from src.component.distributed_lock import DistributeLockExecutor
from src.exceptions import ErroCode, CouponIssueException
from src.repository.redis_repository import CouponIssueRequestDto
from src.repository.redis_repository import RedisRepository
from src.service.coupon_issue_redis_service import CouponIssueRedisService
from src.service.coupon_issue_service import CouPonIssueService
from src.service.coupon_cache_service import CouPonCacheServce
from src.utils import CouponRedisUtils
from src.entity.coupon_redis_entity import CouponRedisEntity


class AsyncCouponIssueService:

    def __init__(self):
        self.repository = RedisRepository()
        self.coupon_issue_redis_serivce = CouponIssueRedisService()
        self.coupon_issue_service = CouPonIssueService()

        self.coupon_cache_service = CouPonCacheServce()

    def issue(self, coupon_id, user_id):
        coupon: CouponRedisEntity = self.coupon_cache_service.get_coupon_cache(coupon_id=coupon_id)
        coupon.check_issuable_coupon()

        # Redis Distribute Lock
        with DistributeLockExecutor(lock_name=f'coupon_{coupon.id}'):
            self.coupon_issue_redis_serivce.check_coupon_issue_quantitiy(
                coupon_redis_entity=coupon,
                user_id=user_id
            )
            self.issue_request(coupon_id=coupon.id, user_id=user_id)

    def issue_request(self, coupon_id, user_id):
        print("issue-request")
        issue_reuqest = CouponIssueRequestDto(coupon_id=coupon_id, user_id=user_id)

        self.repository.client.sadd(CouponRedisUtils.get_issue_request_key(coupon_id), user_id)

        self.repository.rpush(
            CouponRedisUtils.get_issue_request_queue_key(),
            json.dumps(issue_reuqest.to_dict())
        )  # 쿠폰 발급 대기열 큐
