from dependency_injector.wiring import Provide

from settings.container.adapter_container import AWSAdapterContainer


class AbstractS3Storage:
    s3_client = Provide[AWSAdapterContainer.s3_client]
