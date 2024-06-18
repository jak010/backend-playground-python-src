import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy.engine import URL

from adapter.database.engine_factory import SQLALchemyEngineFactory
from src.app.controller import (
    health_router,
    member_router,
    signup_router,
    profile_router,
    session_router,
    auditions_router,
    submission_router
)

load_dotenv()

MODE = os.environ['MODE']

DATABASE = {
    "DRIVERNAME": "mysql+pymysql",
    "USERNAME": os.environ["DB_USER"],
    "PASSWORD": os.environ["DB_PASSWORD"],
    "DATABASE": os.environ["DB_NAME"],
    "HOST": os.environ["DB_HOST"],
    "PORT": int(os.environ["DB_PORT"])
}

AWS = {
    "ACCESS_KEY": os.environ['AWS_ACCESS_KEY'],
    "ACCESS_SECRET_KEY": os.environ['AWS_ACCESS_SECRET_KEY'],
    "REGION_NAME": os.environ['AWS_REGION_NAME'],
    "S3_BUCKET": os.environ['AWS_S3_BUCKET']
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


def patch_ioc():
    from src.config.container.database_container import DataBaseContainer
    from src.config.container.repository_container import RepositoryContainer
    from src.config.container.aws_container import AWSContainer

    packages = ["src.app"]

    db_container = DataBaseContainer(engine=SQLALchemyEngineFactory.get_engine(url=get_db_url()))
    db_container.wire(packages=packages)

    repository_container = RepositoryContainer()
    repository_container.wire(packages=packages)

    aws_container = AWSContainer(
        aws_access_key=AWS['ACCESS_KEY'],
        aws_access_secret_key=AWS['ACCESS_SECRET_KEY'],
        aws_region_name=AWS['REGION_NAME'],
        aws_s3_bucket=AWS['S3_BUCKET']
    )
    aws_container.wire(packages=packages)


def patch_controller(app: FastAPI):
    API_ROUTER = [
        health_router,
        session_router,
        signup_router,
        member_router,
        profile_router,
        auditions_router,
        submission_router
    ]
    for router in API_ROUTER:
        app.include_router(router)


def patch_orm():
    from adapter.database import orm
    from src.app.domain import (
        MemberEntity,
        VerificationEntity,
        ProfileEntity,
        SessionEntity,
        AuditionEntity,
        SubmissionEntity

    )

    from sqlalchemy.orm import registry

    classical_mapping = registry()
    classical_mapping.map_imperatively(MemberEntity, orm.Member)
    classical_mapping.map_imperatively(VerificationEntity, orm.Verification)
    classical_mapping.map_imperatively(ProfileEntity, orm.Profile)
    classical_mapping.map_imperatively(SessionEntity, orm.Session)
    classical_mapping.map_imperatively(AuditionEntity, orm.Audition)
    classical_mapping.map_imperatively(SubmissionEntity, orm.Submission)
