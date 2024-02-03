import random

from locust import task, FastHttpUser, HttpUser
from locust.contrib.fasthttp import ResponseContextManager


class CouponIssueV1(FastHttpUser):
    connection_timeout = 10.0
    network_timeout = 10.0

    @task
    def issue(self):
        payload = {
            "user_id": random.randint(1, 10000000),
            "coupon_id": 1,
        }
        with self.rest("POST", "/api/v1/issue", json=payload) as result:
            if result.status_code != 200 and result.status_code != 400:
                result: ResponseContextManager

                print(result.content)

        # with self.client.post("/api/v1/issue", json=payload, catch_response=True) as response:
        #     if response.status_code != 200 and response.status_code != 400:
        #         print(response.info())
