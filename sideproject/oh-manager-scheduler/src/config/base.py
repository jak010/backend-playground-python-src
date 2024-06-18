import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL

from adapter.database.engine_factory import SQLALchemyEngineFactory

from src.config.container import DataBaseContainer, SlackContainer

load_dotenv()

OPEN_AI_APIKEY = os.environ['OPEN_AI_APIKEY']

DATABASE = {
    "DRIVERNAME": "mysql+pymysql",
    "USERNAME": os.environ["DB_USER"],
    "PASSWORD": os.environ["DB_PASSWORD"],
    "DATABASE": os.environ["DB_NAME"],
    "HOST": os.environ["DB_HOST"],
    "PORT": int(os.environ["DB_PORT"])
}

SLACK = {
    "SLACK_TOKEN": os.environ['SLACK_TOKEN'],
    "SLACK_CHANNEL": os.environ['SLACK_CHANNEL']
}


def get_db_url():
    return URL.create(
        drivername=DATABASE["DRIVERNAME"],
        username=DATABASE["USERNAME"],
        password=DATABASE["PASSWORD"],
        database=DATABASE["DATABASE"],
        host=DATABASE["HOST"],
        port=int(DATABASE["PORT"])
    )


def patch_dependency():
    packages = ["src.app"]

    db_container = DataBaseContainer(engine=SQLALchemyEngineFactory.get_engine(url=get_db_url()))
    db_container.wire(packages=packages)

    slack_container = SlackContainer(slack_token=SLACK['SLACK_TOKEN'], slack_channel=SLACK['SLACK_CHANNEL'])
    slack_container.wire(packages=packages)
