from functools import cached_property

import redis
from redis_lock import Lock


class DistributeLockExecutor:
    _lock = None

    def __init__(self, lock_name: str):
        self.lock_name = lock_name
        self._locked = None

    @cached_property
    def client(self):
        host = "0.0.0.0"
        port = 6379

        redis_pool = redis.ConnectionPool(host=host, port=port, db=1, max_connections=4)
        redis_client = redis.StrictRedis.from_pool(connection_pool=redis_pool)
        return redis_client

    def __enter__(self):
        self._lock = Lock(self.client, self.lock_name)
        self._locked = self._lock.acquire(blocking=True, timeout=10)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._locked:
            self._locked.release()
        self.client.close()
