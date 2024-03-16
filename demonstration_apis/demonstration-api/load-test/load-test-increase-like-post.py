import random

from locust import task, FastHttpUser, between


class LoadtestPostV1(FastHttpUser):
    wait_time = between(5, 15)

    @task
    def issue(self):
        with self.rest("GET", "/api/v1/post") as result:
            if result.status_code == 0:
                print(result.raise_for_status())
