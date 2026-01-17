import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1"
)

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1"
)

for bucket in s3.list_buckets().get('Buckets', []):
    print(bucket['Name'])


for table in dynamodb.tables.all():
    print(table.name)
