from fastapi import FastAPI

from src.controller import ranking_service_router
from src.producer import LeaderBoardProducer

import threading


class BoilerPlateApplication:
    app = FastAPI()

    producer = LeaderBoardProducer()

    def __call__(self, *args, **kwargs):
        t = threading.Thread(target=self.producer.execute, args=())
        t.daemon = True
        t.start()

        self.app.include_router(ranking_service_router)

        return self.app


application = BoilerPlateApplication()
