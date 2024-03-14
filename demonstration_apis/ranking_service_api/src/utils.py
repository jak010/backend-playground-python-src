import redis
from functools import cached_property


class RedisClient:
    HOST = "127.0.0.1"
    PORT = 6380
    DB = 1

    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host=self.HOST,
            port=self.PORT,
            db=self.DB,
            decode_responses=True
        )

    @cached_property
    def client(self) -> redis.StrictRedis:
        return self.redis_client
