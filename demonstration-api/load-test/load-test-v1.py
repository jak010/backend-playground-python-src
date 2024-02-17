import random

from locust import task, FastHttpUser


class LoadtestV1(FastHttpUser):
    connection_timeout = 10
    network_timeout = 10

    @task
    def issue(self):
        payload = {
            "user_id": random.randint(1, 10000000),
            "coupon_id": 1,
        }
        with self.rest("POST", "/api/v1", json=payload) as result:
            if result.status_code == 0:
                print(result.raise_for_status())
