import base64
import os

import boto3
from datetime import datetime as dt
import json
import timestamp_random as tr
import ingest.filters as filters


def handler(event, context):
    client = boto3.resource("dynamodb")
    table_name = os.getenv("DATAPLATTFORM_RAW_TABLENAME")
    table = client.Table(table_name)

    data_type = event["pathParameters"]["type"]
    data = (event["body"])
    timestamp, timestamp_random = insert_doc(table, data_type, data=data)
    return {
        'statusCode': 200,
        'body': json.dumps({
            "timestamp": timestamp,
            "id": base64.b64encode(timestamp_random).decode("utf-8")
        })
    }


def insert_doc(table, type, data=None, timestamp=None):
    if type in filters.filter:
        data = filters.filter[type](data)
    if data is None:
        return 0
    if timestamp is None:
        timestamp = int(dt.now().timestamp())

    timestamp_random = tr.get_timestamp_random()
    item = {
        "type": type,
        "timestamp_random": timestamp_random,
        "timestamp": timestamp
    }
    if data is not None:
        item["data"] = data

    table.put_item(
        Item=item
    )

    return timestamp, timestamp_random
