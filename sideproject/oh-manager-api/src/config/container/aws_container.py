from dependency_injector import providers, containers
from mypy_boto3_s3 import S3Client

from adapter.aws.s3.client import get_s3_client


class AWSContainer(containers.DeclarativeContainer):
    aws_access_key = providers.Dependency()
    aws_access_secret_key = providers.Dependency()
    aws_region_name = providers.Dependency()

    aws_s3_bucket = providers.Dependency()

    s3_client: providers.Provider[S3Client] = providers.Singleton(
        get_s3_client,
        aws_access_key=aws_access_key,
        aws_access_secret_key=aws_access_secret_key,
        region_name=aws_region_name
    )
