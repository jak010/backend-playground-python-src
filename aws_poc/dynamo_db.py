import boto3

from mypy_boto3_dynamodb import DynamoDBServiceResource, DynamoDBClient

endpoint = "http://127.0.0.1:4566"  # localstack

resource: DynamoDBServiceResource = boto3.resource('dynamodb', endpoint_url=endpoint)
client: DynamoDBClient = boto3.client('dynamodb', endpoint_url=endpoint)

# table = resource.Table("TestTable")
schema = {
    'TableName': 'TestTable',
    'KeySchema': [
        {
            'AttributeName': 'name',
            'KeyType': 'HASH'  # Partition key
        },
    ],
    'AttributeDefinitions': [
        {
            'AttributeName': 'name',
            'AttributeType': 'S'
        },
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
}
# resource.create_table(**schema)
# print(client.list_tables())

from boto3.dynamodb.conditions import Key

table = resource.Table("TestTable")
query = {"KeyConditionExpression": Key("name").eq("키값")}
print(table.query(**query))
