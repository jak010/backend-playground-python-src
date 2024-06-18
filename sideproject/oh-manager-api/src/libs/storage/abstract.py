from abc import ABCMeta, abstractmethod

from dependency_injector.wiring import Provide
from mypy_boto3_s3 import S3Client

from src.config.container.aws_container import AWSContainer


class AbstractStorage(metaclass=ABCMeta):
    s3_storage: S3Client = Provide[AWSContainer.s3_client]

    s3_bucket = Provide[AWSContainer.aws_s3_bucket]
