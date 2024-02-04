import redis
from redis_lock import RedisSpinLock, RedisLock
from typing import Callable


class DistributeLockExecutor:

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 6379
        self.db = 1
        self.client = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

        self._lock = None

    def acquire(self, lock_name) -> RedisLock:
        """ acquire """
        self._lock = RedisLock(self.client, lock_name, expire_timeout=60)

        return self._lock.acquire()

    def release(self):
        if self._lock:
            self._lock.release()

    # def execute(self, lock_name, wait_time=10, func: Callable = None):
    #     lock = RedisLock(self.client, lock_name, expire=60)
    #
    #     if not lock.acquire():
    #         raise Exception("Faile To Acquire Lock")
    #
    #     result = func()
    #
    #     lock.release()
