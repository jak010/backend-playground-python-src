from src.repository.redis_repository import RedisRepository
from src.utils import CouponRedisUtils
from src.entity.coupon_redis_entity import CouponRedisEntity
from src.exceptions import CouponIssueException, ErroCode


class CouponIssueRedisService:

    def __init__(self):
        self.repository = RedisRepository()

    def check_coupon_issue_quantitiy(self, coupon_redis_entity: CouponRedisEntity, user_id: int):
        if not self.available_user_issue_quantity(coupon_id=coupon_redis_entity.id, user_id=user_id):
            raise CouponIssueException(ErroCode.DUPLICATE_COUPON_ISSUE, f"발급 가능 수량을 초과했다.")

        if not self.available_total_issue_quantity(total_quantity=coupon_redis_entity.total_quantity, coupon_id=coupon_redis_entity.id):
            raise CouponIssueException(ErroCode.INVALID_COUPON_ISSUE_QUANTITY, f"발급 가능한 수량을 초과합니다")

    def available_total_issue_quantity(self, total_quantity: int, coupon_id: int) -> bool:
        if total_quantity is None:
            return True

        key = CouponRedisUtils.get_issue_request_key(coupon_id)
        return total_quantity > self.repository.scard(key)

    def available_user_issue_quantity(self, coupon_id: int, user_id: int) -> bool:
        key = CouponRedisUtils.get_issue_request_key(int(coupon_id))
        return not self.repository.sismember(key=key, value=str(user_id))
