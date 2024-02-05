import redis


class RedisWorker:
    host = "localhost"
    port = 6379
    db = 1

    queue_name = "test:queue"

    @property
    def client(self):
        return redis.StrictRedis(host=self.host, port=self.port, db=self.db)

    @property
    def _queue_size(self) -> int:
        return self.client.llen(name=self.queue_name)

    @property
    def is_empty(self) -> bool:
        return self._queue_size == 0
