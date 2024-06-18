import boto3


def get_s3_client(aws_access_key: str, aws_access_secret_key: str, region_name: str) -> boto3:
    return boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_access_secret_key,
        region_name=region_name
    )
