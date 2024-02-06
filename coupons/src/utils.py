import datetime
from functools import wraps
import redis
import dataclasses
from src.entity.coupon_redis_entity import CouponRedisEntity


class CouponRedisUtils:

    @staticmethod
    def get_issue_request_key(coupon_id: str):
        return f'issue.request.coupon_id={coupon_id}'

    @staticmethod
    def get_issue_request_queue_key():
        return f"issue.request"


class Cacheable:

    def __init__(self, cache_name: str):
        self.cache_name = cache_name

        self.host = "127.0.0.1"
        self.port = 6379
        self.db = 1
        self.client = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if dataclasses.is_dataclass(result):
                self.client.sadd(self.cache_name, result.to_json())
                return result

        return wrapper
