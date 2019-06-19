import boto3
import random
from datetime import datetime as dt
import json


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


def get_timestamp_random(timestamp=None, random_value=None):
    """
    :param random_value: You can choose a specific value instead of generating a random one.
    :param timestamp: A specific unix timestamp, keep None if you want to use current time.
    :return: timestamp in bits appended with some random bits as a Binary.
    """

    def to_byte_array(number: int, bytes: int = 16):
        return number.to_bytes(bytes, 'big')

    if timestamp is None:
        timestamp = int(dt.now().timestamp())

    if random_value is None:
        random_value = random.getrandbits(64)

    return to_byte_array((timestamp << 64) + random_value, 16)


def insert_doc(table, type, data=None, timestamp=None):
    if timestamp is None:
        timestamp = int(dt.now().timestamp())

    item = {
        "type": type,
        "timestamp_random": get_timestamp_random(timestamp),
        "timestamp": timestamp
    }
    if data is not None:
        item["data"] = data

    table.put_item(
        Item=item
    )

    return timestamp
