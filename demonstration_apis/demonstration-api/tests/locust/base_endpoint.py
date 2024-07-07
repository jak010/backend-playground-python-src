import random

from locust import task, FastHttpUser, between


class LoadtestPostV1(FastHttpUser):

    @task
    def issue(self):
        self.client.get("/api/v1/asyncio")
