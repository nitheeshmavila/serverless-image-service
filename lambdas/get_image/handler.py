
import json
import boto3
from botocore.config import Config

LOCALSTACK_ENDPOINT = "http://localstack:4566"
TABLE_NAME = "ImagesTable"

s3 = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name="us-east-1",
    config=Config(s3={"addressing_style": "path"})
)

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name="us-east-1"
)

table = dynamodb.Table(TABLE_NAME)


def handler(event, context):
    image_id = event["pathParameters"]["image_id"]

    # Fetch metadata from DB
    response = table.get_item(Key={"image_id": image_id})

    if "Item" not in response:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Image not found"})
        }

    item = response["Item"]

    # Generate pre-signed URL
    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": item["s3_bucket"],
            "Key": item["s3_key"]
        },
        ExpiresIn=300
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "image_id": image_id,
            "download_url": presigned_url
        })
    }
