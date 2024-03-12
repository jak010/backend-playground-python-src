from config.settings import redis_client
from src.entity.coupon_redis_entity import CouponRedisEntity
from src.service.coupon_issue_service import CouPonIssueService
from src.utils import CouponCacheLookAside


class CouPonCacheServce:
    coupon_issue_service = CouPonIssueService()

    cache_client = redis_client()

    @CouponCacheLookAside(cache_name='coupons')
    def get_coupon_cache(self, coupon_id: int) -> CouponRedisEntity:
        coupon = self.coupon_issue_service.find_coupon(coupon_id=coupon_id)
        return CouponRedisEntity.of(coupon=coupon)
