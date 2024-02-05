import json

from src.component.distributed_lock import DistributeLockExecutor
from src.entity.coupon_entity import CouponIssueException, ErroCode
from src.repository.redis_repository import CouponIssueRequestDto
from src.repository.redis_repository import RedisRepository
from src.service.coupon_service import CouPonIssueService
from src.utils import CoutponRedisUtils


class CouponIssueRedisService:

    def __init__(self):
        self.repository = RedisRepository()

    def available_user_issue_quantity(self, coupon_id, user_id) -> bool:
        key = CoutponRedisUtils.get_issue_request_key(coupon_id)
        return not self.repository.sismember(key=key, value=user_id)

    def available_total_issue_qunatity(self, total_quantity: int, coupon_id: int) -> bool:
        if total_quantity is None:
            return True

        key = CoutponRedisUtils.get_issue_request_key(coupon_id)
        return total_quantity > self.repository.scard(key)


class AsyncCouponIssueService:

    def __init__(self):
        self.repository = RedisRepository()
        self.coupon_issue_redis_serivce = CouponIssueRedisService()
        self.coupon_issue_service = CouPonIssueService()

    def issue(self, coupon_id, user_id):
        coupon = self.coupon_issue_service.find_coupon(coupon_id=coupon_id)

        if not coupon.avaliable_issue_date():
            raise CouponIssueException(ErroCode.INVALID_COUPON_ISSUE_DATE, "발급 가능한 일자가 아닙니다.")

        lock = DistributeLockExecutor()
        if lock.acquire(lock_name=f'coupon_{coupon.id}'):

            if not self.coupon_issue_redis_serivce.available_total_issue_qunatity(total_quantity=coupon.total_quantity, coupon_id=coupon.id):
                raise CouponIssueException(ErroCode.INVALID_COUPON_ISSUE_QUANTITY, f"발급 가능 수량을 초과했다.")

            if not self.coupon_issue_redis_serivce.available_user_issue_quantity(coupon_id=coupon_id, user_id=user_id):
                raise CouponIssueException(ErroCode.DUPLICATE_COUPON_ISSUE, f"이미 발급 요청이 처리됐습니다.")
            self.issue_request(coupon_id=coupon.id, user_id=user_id)
        lock.release()

    def issue_request(self, coupon_id, user_id):
        issue_reuqest = CouponIssueRequestDto(coupon_id=coupon_id, user_id=user_id)

        self.repository.client.sadd(CoutponRedisUtils.get_issue_request_key(coupon_id), user_id)
        self.repository.rpush(
            CoutponRedisUtils.get_issue_request_queue_key(),
            json.dumps(issue_reuqest.to_dict())
        )  # 쿠폰 발급 대기열 큐
