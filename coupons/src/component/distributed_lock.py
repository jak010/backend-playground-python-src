import redis
from redis_lock import RedisLock


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
