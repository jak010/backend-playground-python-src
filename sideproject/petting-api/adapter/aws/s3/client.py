import boto3

from mypy_boto3_s3 import S3ServiceResource


class S3Client:

    def __init__(self,
                 aws_access_key,
                 aws_access_secret_key,
                 region_name,
                 bucket_name,
                 ):
        self.s3: S3ServiceResource = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_access_secret_key,
            region_name=region_name
        )
        self._bucket_name = bucket_name

    def bucket(self):
        return self.s3.Bucket(name=self._bucket_name)
