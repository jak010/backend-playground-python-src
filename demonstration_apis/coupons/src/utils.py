import dataclasses
import json
from functools import wraps

from config.settings import redis_client
from src.entity.coupon_redis_entity import CouponRedisEntity


class CouponRedisUtils:

    @staticmethod
    def get_issue_request_key(coupon_id: str):
        return f'issue.request.coupon_id={coupon_id}'

    @staticmethod
    def get_issue_request_queue_key():
        return f"issue.request"


class CouponCacheLookAside:
    def __init__(self, cache_name: str):
        self.cache_name = cache_name
        self.client = redis_client()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            coupon_id = kwargs.get('coupon_id', None)

            if coupon_id is not None:
                cached_datas = self.client.smembers(name=self.cache_name)
                if cached_datas:
                    for cached_data in cached_datas:
                        data = json.loads(cached_data.decode())
                        if data['id'] == coupon_id:
                            return CouponRedisEntity(**data)

            result = func(*args, **kwargs)
            if dataclasses.is_dataclass(result):
                self.client.sadd(self.cache_name, result.to_json())
                return result

        return wrapper


class Cacheable:

    def __init__(self, cache_name: str):
        self.cache_name = cache_name

        self.client = redis_client()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if dataclasses.is_dataclass(result):
                self.client.sadd(self.cache_name, result.to_json())
                return result

        return wrapper
