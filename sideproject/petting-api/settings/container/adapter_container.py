from dependency_injector import providers, containers

from adapter.aws.s3.client import S3Client
from adapter.kakao import (
    KaKaoApi,
    KaKaoConfig
)
from adapter.aligo import SMSApi


class KaKaoAdapterContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=['src']
    )
    client_id = providers.Dependency()
    client_secret = providers.Dependency()
    redirect_uri = providers.Dependency()

    _config = providers.Singleton(
        KaKaoConfig,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )

    kako_api: KaKaoApi = providers.Singleton(
        KaKaoApi,
        kakao_config=_config
    )


class AWSAdapterContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=['src']
    )

    aws_access_key = providers.Dependency()
    aws_access_secret_key = providers.Dependency()
    aws_region_name = providers.Dependency()
    aws_s3_bucket = providers.Dependency()

    s3_client: S3Client = providers.Singleton(
        S3Client,
        aws_access_key=aws_access_key,
        aws_access_secret_key=aws_access_secret_key,
        region_name=aws_region_name,
        bucket_name=aws_s3_bucket
    )


class AligoAdapterContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=['src']
    )

    mode = providers.Dependency()
    aligo_api_key = providers.Dependency()
    aligo_user_id = providers.Dependency()
    aligo_sender = providers.Dependency()

    sms_api = providers.Singleton(
        SMSApi,
        mode=mode,
        aligo_api_key=aligo_api_key,
        aligo_user_id=aligo_user_id,
        aligo_sender=aligo_sender
    )
