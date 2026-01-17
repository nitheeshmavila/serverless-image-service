import json
import uuid
import base64
import datetime
import boto3
from botocore.config import Config

LOCALSTACK_ENDPOINT = "http://localstack:4566"

BUCKET_NAME = "images-bucket"
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
    print("EVENT:", event)

    body = json.loads(event.get("body") or "{}")

    image_id = str(uuid.uuid4())
    user_id = body["user_id"]

    image_bytes = base64.b64decode(body["image_base64"])

    s3_key = f"{user_id}/{image_id}_{body['filename']}"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=image_bytes,
        ContentType=body.get("content_type", "image/jpeg")
    )

    table.put_item(
        Item={
            "image_id": image_id,
            "user_id": user_id,
            "filename": body["filename"],
            "tags": body.get("tags", []),
            "created_at": datetime.datetime.utcnow().isoformat(),
            "s3_bucket": BUCKET_NAME,
            "s3_key": s3_key
        }
    )

    return {
        "statusCode": 201,
        "body": json.dumps({
            "image_id": image_id,
            "message": "Image uploaded successfully"
        })
    }
