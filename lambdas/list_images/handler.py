import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

LOCALSTACK_ENDPOINT = "http://localstack:4566"
TABLE_NAME = "ImagesTable"

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name="us-east-1"
)

table = dynamodb.Table(TABLE_NAME)


def handler(event, context):
    params = event.get("queryStringParameters") or {}

    user_id = params.get("user_id")
    tag = params.get("tag")
    from_date = params.get("from")
    to_date = params.get("to")

    if not user_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "user_id is required"})
        }

    key_condition = Key("user_id").eq(user_id)
    if from_date and to_date:
        key_condition &= Key("created_at").between(from_date, to_date)
    elif from_date:
        key_condition &= Key("created_at").gte(from_date)
    elif to_date:
        key_condition &= Key("created_at").lte(to_date)

    response = table.query(
        IndexName="user_id-created_at-index",
        KeyConditionExpression=key_condition
    )

    items = response.get("Items", [])

    # tag filter
    if tag:
        items = [
            item for item in items
            if tag in item.get("tags", [])
        ]

    return {
        "statusCode": 200,
        "body": json.dumps(items)
    }
