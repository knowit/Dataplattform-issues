import boto3
from datetime import datetime as dt
import json
import timestamp_random as tr


def lambda_handler(event, context):
    client = boto3.resource("dynamodb")
    table = client.Table("dataplattform")

    data_type = event["pathParameters"]["type"]
    data = (event["body"])
    timestamp = insert_doc(table, data_type, data=data)
    return {
        'statusCode': 200,
        'body': json.dumps({"timestamp": timestamp})
    }


def insert_doc(table, type, data=None, timestamp=None):
    if timestamp is None:
        timestamp = int(dt.now().timestamp())

    item = {
        "type": type,
        "timestamp_random": tr.get_timestamp_random(timestamp),
        "timestamp": timestamp
    }
    if data is not None:
        item["data"] = data

    table.put_item(
        Item=item
    )

    return timestamp
