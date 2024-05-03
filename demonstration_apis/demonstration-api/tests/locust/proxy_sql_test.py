import random

from locust import task, FastHttpUser, between


class LoadtestPostV1(FastHttpUser):
    connection_timeout = 10.0
    network_timtout = 10.9

    @task
    def issue(self):
        self.client.get("/api/v1/test")
