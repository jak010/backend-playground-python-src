from .abstract import RedisWorker


class RedisConsumer(RedisWorker):

    def get_data(self):
        if not self.is_empty:
            return self.client.rpop(name=self.queue_name)


if __name__ == '__main__':
    consumer = RedisConsumer()

    while True:
        import time

        time.sleep(0.5)
        if not consumer.empty():
            print("task ...")
            data = consumer.get_data()
        else:
            print("listen ...")
