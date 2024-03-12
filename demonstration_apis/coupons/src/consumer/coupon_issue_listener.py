import time

from src.repository.redis_repository import RedisRepository, CouponIssueRequestDto
from src.service.coupon_issue_service import CouPonIssueService

from config.logger import UVICORN_SYSOUT_LOGGER
from src.utils import CouponRedisUtils


class CouponIssueListener:
    redis_repository = RedisRepository()
    coupon_issue_service = CouPonIssueService()

    queue_key = CouponRedisUtils.get_issue_request_queue_key()

    def issue(self):
        UVICORN_SYSOUT_LOGGER.info("listen ...")
        while self.exist_coupon_issue_target():
            time.sleep(1)

            target = self.get_issue_target()
            UVICORN_SYSOUT_LOGGER.info(f" 발급 시작...{target}")
            self.coupon_issue_service.issue(coupon_id=target.coupon_id, user_id=target.user_id)
            UVICORN_SYSOUT_LOGGER.info(f" 발급 완료...{target}")
            self.redis_repository.lpop(key=self.queue_key)

    def exist_coupon_issue_target(self) -> bool:
        return self.redis_repository.lsize(key=self.queue_key) > 0

    def get_issue_target(self):
        import json
        data = self.redis_repository.lindex(key=self.queue_key, index=0).decode()
        data = json.loads(data)

        return CouponIssueRequestDto(coupon_id=data['coupon_id'], user_id=data['user_id'])

    def remove_issued_target(self):
        self.redis_repository.lpop(key=self.queue_key)
