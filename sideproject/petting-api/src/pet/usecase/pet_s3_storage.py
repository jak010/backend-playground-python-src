from functools import cached_property
from io import BytesIO

from mypy_boto3_s3.service_resource import Bucket

from libs.abstract.abstract_s3_storage import AbstractS3Storage
from libs.utils import file_utils
from settings.config.base import ExecuteEnviorment
from src.member.entity import MemberEntity


class PetImageStorage(AbstractS3Storage):

    @cached_property
    def bucket(self) -> Bucket:
        return self.s3_client.bucket()

    def upload_pets_image(self,
                          owner: MemberEntity,
                          upload_name: str,
                          attachment_label: str,
                          content_type: str,
                          file: BytesIO,
                          ):
        upload_key = f"{owner.email}/image/{attachment_label}/{file_utils.normailize_file_name(upload_name)}"
        if ExecuteEnviorment.MODE == 'LOCAL':
            return upload_key

        self.bucket.upload_fileobj(
            Key=upload_key,
            Fileobj=file,
            ExtraArgs={"ContentType": content_type},
        )
        return upload_key
