import redis
from functools import cached_property
import dataclasses


@dataclasses.dataclass
class CouponIssueRequestDto:
    coupon_id: int
    user_id: int

    def to_dict(self):
        return dataclasses.asdict(self)

class RedisRepository:

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 6379
        self.db = 1
        self.client = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

    def zadd(self, key: str, value: dict) -> bool:
        return self.client.zadd(key, value, nx=True)  # NX: 데이터가 없는경우만 처리 , 있는경우 무시

    def sadd(self, key: str, value: str):
        return self.client.sadd(key, value)

    def scard(self, key: str):
        return self.client.scard(key)

    def sismember(self, key, value):
        return self.client.sismember(key, value)

    # queue
    def rpush(self, key, value):
        return self.client.rpush(key, value)

    def lpop(self, key):
        return self.client.lpop(key)

    def clear(self, key):
        return self.client.delete(key)
