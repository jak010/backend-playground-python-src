import redis
from redis_lock import Lock
from functools import cached_property
import os


class DistributeLockExecutor:

    def __init__(self, lock_name: str):
        self._lock = Lock(self.client, lock_name)
        self._is_lock = None

    @property
    def client(self):
        host = "127.0.0.1"
        port = 6379
        db = 1
        r = redis.Redis(host=host, port=port, db=db, socket_connect_timeout=1)
        return r

    def __enter__(self):
        self._is_lock = self._lock.acquire(blocking=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._lock:
            self._lock.release()
        self.client.close()
