import random

from locust import task, FastHttpUser


class CouponIssueV1(FastHttpUser):
    connection_timeout = 10.0
    network_timeout = 10.0

    @task
    def issue(self):
        payload = {
            "user_id": random.randint(1, 10000000),
            "coupon_id": 1,
        }
        with self.rest("POST", "/api/v1/issue", json=payload):
            pass
