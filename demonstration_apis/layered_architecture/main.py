import threading

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from src.member.api import member_router

from library.abstract import AbstractRdbRepsitory
from external_library.database import SQLAlchemyConnector
from sqlalchemy.engine import URL
from functools import wraps

from external_library.database import SQLAlchemyConnector
from settings.enviornment import DataBaseEnviroment
from external_library.orm import Member

import threading


def connection_poolup(
        app
        # sqla=Depends(SQLAlchemyConnector)
):
    connector = SQLAlchemyConnector.with_url(url=DataBaseEnviroment.get_uri())
    session = connector.get_session()
    # session.execute("select 1;")

    AbstractRdbRepsitory.session = connector.get_session()

    [threading.Thread(target=session.execute("select 1;")) for _ in range(5)]

    yield

    engine = connector.get_engine()
    engine.dispose()


class LayeredArchitecture:
    app = FastAPI(
        title="Demo Layerd Archtecture",
        description=""" Some,
        """,
        lifespan=connection_poolup

    )

    def __call__(self, *args, **kwargs):
        self.app.include_router(member_router)

        return self.app


application = LayeredArchitecture()
