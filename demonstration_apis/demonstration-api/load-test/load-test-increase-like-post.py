import random

from locust import task, FastHttpUser


class LoadtestPostV1(FastHttpUser):
    connection_timeout = 10
    network_timeout = 10

    @task
    def issue(self):
        with self.rest("GET", "/api/v1/post") as result:
            if result.status_code == 0:
                print(result.raise_for_status())
