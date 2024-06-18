import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import (
    setup,
    scheduler
)
from src.config.logger import sql_logger

load_dotenv()

MODE = os.environ['MODE']

if MODE != "DEPLOY":
    SQL_LOGGER = logging.getLogger("sqlalchemy.engine.Engine")
    SQL_LOGGER.addHandler(sql_logger.get_handler())


# Application Entry
class Application:

    def __init__(self):
        self.app = FastAPI()

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Setup
        setup.add_controller(self.app)
        setup.add_database(db={
            "username": os.environ['MYSQL_USER'],
            "password": os.environ['MYSQL_PASSWORD'],
            "database": os.environ['MYSQL_NAME'],
            "host": os.environ['MYSQL_HOST'],
            "port": os.environ['MYSQL_PORT']
        })
        setup.orm_dispatch()

    def __call__(self, *args, **kwargs):
        if MODE == "DEPLOY":
            scheduler.periodic().start()

        return self.app


server = Application()
