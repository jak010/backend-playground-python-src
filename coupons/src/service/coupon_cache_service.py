from src.service.coupon_issue_service import CouPonIssueService
from src.entity.coupon_redis_entity import CouponRedisEntity

from src.utils import Cacheable


class CouPonCacheServce:
    coupon_issue_service = CouPonIssueService()

    @Cacheable(cache_name='coupons')
    def get_coupon_cache(self, coupon_id: int) -> CouponRedisEntity:
        coupon = self.coupon_issue_service.find_coupon(coupon_id=coupon_id)
        return CouponRedisEntity.of(coupon=coupon)

