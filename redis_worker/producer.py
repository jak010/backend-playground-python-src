import json
import uuid

from .abstract import RedisWorker


class RedisProducer(RedisWorker):

    def push(self, data: dict):
        return self.client.lpush(self.queue_name, json.dumps(data))


if __name__ == '__main__':
    producer = RedisProducer()

    while True:
        import time

        time.sleep(1)
        producer.push(data={"user_id": str(uuid.uuid4())})
        print("insert ...")
