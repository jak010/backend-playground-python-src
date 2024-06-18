from .abstract import AbstractStorage
from src.config.settings import base


class MemberStorage(AbstractStorage):

    @classmethod
    def get_link(cls, profile_url: str):
        s3_url = f'https://{cls.s3_bucket}.s3.amazonaws.com/{profile_url}'
        return s3_url

    @classmethod
    def upload_member_profile(
            cls,
            member_id: str,
            file_name: str,
            file_content: bytes,
            content_type: str
    ):
        save_key = member_id + "/" + file_name
        cls.s3_storage.put_object(
            Bucket=cls.s3_bucket,
            Key=save_key,
            Body=file_content,
            ContentType=content_type
        )
        return save_key

    @classmethod
    def create_member_storage(cls, member_id: str):
        """ Member 개인, 저장 공간 생성 """
        if base.MODE == "LOCAL": # TODO, 24.01.28, 리팩토핑 필요함
            return True

        save_key = member_id + "/"
        cls.s3_storage.put_object(
            Key=save_key,
            Bucket=cls.s3_bucket
        )
