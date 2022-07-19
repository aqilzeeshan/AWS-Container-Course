import boto3
import os
"""
aws dynamodb create-table --table-name Employees \
 --attribute-definitions AttributeName=id,AttributeType=S \
 --key-schema AttributeName=id,KeyType=HASH \
 --billing-mode PAY_PER_REQUEST \
 --endpoint-url http://localhost:8000
"""

DYNAMO_ENDPOINT_OVERRIDE = os.getenv('DYNAMO_ENDPOINT_OVERRIDE', None)
config = {'endpoint_url': DYNAMO_ENDPOINT_OVERRIDE} if DYNAMO_ENDPOINT_OVERRIDE else {}
dynamodb = boto3.resource('dynamodb', **config)

table = dynamodb.create_table(
    TableName='Employees',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        }
    ],
    BillingMode="PAY_PER_REQUEST"
)