# awslocal-cli

```sh
$ pip install awscli-local
```

# EC2 Command

- `Create, EC2 Pem Key`
    ```sh
    $ awslocal ec2 create-key-pair --key-name my-key --query 'KeyMaterial' --output text | tee key.pem
    $ chmod 400 key.pem
    ```

    - Run, EC2 Instance
      ```sh
      awslocal ec2 run-instances \
          --image-id ami-ff0fea8310f3 \
          --count 1 \
          --instance-type t3.nano \
          --key-name my-key \
          --security-group-ids 'sg-7365b6be6c6f5d1c5'
      ```
    - Example
      ```json
      {
      "Groups": [
          {
              "GroupName": "default",
              "GroupId": "sg-245f6a01"
          }
      ],
      "Instances": [
          {
              "AmiLaunchIndex": 0,
              "ImageId": "ami-ff0fea8310f3",
              "InstanceId": "i-578503563f8532361",
              "InstanceType": "t3.nano",
              "KernelId": "None",
              "KeyName": "my-key",
              "LaunchTime": "2024-05-04T16:12:56+00:00",
              "Monitoring": {
                  "State": "disabled"
              },
              "Placement": {
                  "AvailabilityZone": "ap-northeast-2a",
                  "GroupName": "",
                  "Tenancy": "default"
              },
              "PrivateDnsName": "ip-10-148-76-225.ap-northeast-2.compute.internal",
              "PrivateIpAddress": "10.148.76.225",
              "PublicDnsName": "ec2-54-214-38-41.ap-northeast-2.compute.amazonaws.com",
              "PublicIpAddress": "54.214.38.41",
              "State": {
                  "Code": 0,
                  "Name": "pending"
              },
              "StateTransitionReason": "",
              "SubnetId": "subnet-97257ff6",
              "VpcId": "vpc-8dd44944",
              "Architecture": "x86_64",
              "BlockDeviceMappings": [
                  {
                      "DeviceName": "/dev/sda1",
                      "Ebs": {
                          "AttachTime": "2024-05-04T16:12:56+00:00",
                          "DeleteOnTermination": false,
                          "Status": "in-use",
                          "VolumeId": "vol-8ad7c508"
                      }
                  }
              ],
              "ClientToken": "ABCDE0000000000003",
              "EbsOptimized": false,
              "Hypervisor": "xen",
              "NetworkInterfaces": [
                  {
                      "Association": {
                          "IpOwnerId": "000000000000",
                          "PublicIp": "54.214.38.41"
                      },
                      "Attachment": {
                          "AttachTime": "2015-01-01T00:00:00+00:00",
                          "AttachmentId": "eni-attach-e0039b20",
                          "DeleteOnTermination": true,
                          "DeviceIndex": 0,
                          "Status": "attached"
                      },
                      "Description": "Primary network interface",
                      "Groups": [
                          {
                              "GroupName": "default",
                              "GroupId": "sg-41aec5a31a1fd27c4"
                          }
                      ],
                      "MacAddress": "1b:2b:3c:4d:5e:6f",
                      "NetworkInterfaceId": "eni-d660c313",
                      "OwnerId": "000000000000",
                      "PrivateIpAddress": "10.148.76.225",
                      "PrivateIpAddresses": [
                          {
                              "Association": {
                                  "IpOwnerId": "000000000000",
                                  "PublicIp": "54.214.38.41"
                              },
                              "Primary": true,
                              "PrivateIpAddress": "10.148.76.225"
                          }
                      ],
                      "SourceDestCheck": true,
                      "Status": "in-use",
                      "SubnetId": "subnet-97257ff6",
                      "VpcId": "vpc-8dd44944"
                  }
              ],
              "RootDeviceName": "/dev/sda1",
              "RootDeviceType": "ebs",
              "SecurityGroups": [
                  {
                      "GroupName": "default",
                      "GroupId": "sg-41aec5a31a1fd27c4"
                  }
              ],
              "SourceDestCheck": true,
              "StateReason": {
                  "Code": "",
                  "Message": ""
              },
              "VirtualizationType": "paravirtual"
          }
      ],
      "OwnerId": "000000000000",
      "ReservationId": "r-25f7ed9d"
  
      }
      ```

# AMI IMAGE 조회하기

```sh
$ awslocal ec2 describe-images
```

# Secutiry Group, 관련

## Security Group, Ingress 설정

```sh
$ awslocal ec2 authorize-security-group-ingress --group-id default --protocol tcp --port 8000 --cidr 0.0.0.0/0
```

- Example

  ```json
  {
  "Return": true,
  "SecurityGroupRules": [
    {
      "SecurityGroupRuleId": "sgr-e49532d6abfbffed1",
      "GroupId": "sg-41aec5a31a1fd27c4",
      "GroupOwnerId": "000000000000",
      "IsEgress": false,
      "IpProtocol": "tcp",
      "FromPort": 8000,
      "ToPort": 8000,
      "CidrIpv4": "0.0.0.0/0",
      "Description": "",
      "Tags": []
    }
  ]

  }
  ```

## Security Group 목록

```sh
$ awslocal ec2 describe-security-groups
```

- Example
    ```json
    {
      "SecurityGroups": [
        {
          "Description": "default VPC security group",
          "GroupName": "default",
          "IpPermissions": [],
          "OwnerId": "000000000000",
          "GroupId": "sg-41aec5a31a1fd27c4",
          "IpPermissionsEgress": [
            {
              "IpProtocol": "-1",
              "IpRanges": [
                {
                  "CidrIp": "0.0.0.0/0"
                }
              ],
              "Ipv6Ranges": [],
              "PrefixListIds": [],
              "UserIdGroupPairs": []
            }
          ],
          "Tags": [],
          "VpcId": "vpc-8dd44944"
        }
      ]
    }
    
    ```

## 1번 Seucrity Group 대상으로 보안그룹 ID 얻어오기

```sh
$ awslocal ec2 describe-security-groups | jq -r '.SecurityGroups[0] | .GroupId'
```