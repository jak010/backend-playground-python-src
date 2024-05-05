"""
LocalStack, EC2 Running 상태인 Instnace를 Terminate 시키기

"""

import boto3

from mypy_boto3_ec2 import EC2Client

REGION = 'ap-northeast-2'

ec2: EC2Client = boto3.client(
    'ec2',
    region_name=REGION,
    endpoint_url='http://localhost:4566'
)

describe_instances = ec2.describe_instances()

target = []
for reservation in describe_instances['Reservations']:
    instances = reservation['Instances']

    for instance in instances:
        if instance['State']['Name'] == 'running':
            target.append(instance['InstanceId'])

r = ec2.terminate_instances(InstanceIds=target)
print(r)
