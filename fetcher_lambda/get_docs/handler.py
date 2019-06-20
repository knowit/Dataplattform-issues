import boto3
import random
from datetime import datetime as dt
from boto3.dynamodb.conditions import Key
import json
import base64


def lambda_handler(event, context):
    client = boto3.resource("dynamodb")
    table = client.Table("dataplattform")

    data_type = event["pathParameters"]["type"]
    params = event["queryStringParameters"]

    timestamp_from = 0
    timestamp_to = 2147483647
    if params:
        if "timestamp_from" in params:
            timestamp_from = int(params["timestamp_from"])
        if "timestamp_to" in params:
            timestamp_to = int(params["timestamp_to"])
        else:
            # Todo some error message here, wrong parameters.
            pass
    docs = get_docs(table, data_type, timestamp_from, timestamp_to)
    docs = docs_to_json(docs)
    return {
        'statusCode': 200,
        'body': json.dumps(docs)
    }


def docs_to_json(docs):
    """
    :param docs: raw docs from DynamoDB
    :return: Convert boto types to regular ints and strings and then parse every doc to json.
    """
    for doc in docs:
        doc["timestamp_random"] = str(base64.b64encode(doc["timestamp_random"].value))
        doc["timestamp"] = int(doc["timestamp"])
        doc["data"] = json.loads(doc["data"])
    return docs


def get_docs(table, data_type, timestamp_from, timestamp_to):
    """
    :param table: DynamoDB table.
    :param data_type: Which type of documents should be fetched.
    :param timestamp_from: Start unix time.
    :param timestamp_to: end unix time. 
    :return: A list of all documents found.
    """
    lower_value = get_range_timestamp_random(timestamp_from)[0]
    upper_value = get_range_timestamp_random(timestamp_to)[1]

    response = table.query(
        KeyConditionExpression=Key('timestamp_random').between(lower_value, upper_value) & Key(
            'type').eq(data_type),
    )
    items = response['Items']
    return items


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


def get_range_timestamp_random(timestamp: int):
    """
    :param timestamp: Unix timestamp
    :return: A range of possible values a timestamp can get from get_timestamp_random().
    """

    lowest = get_timestamp_random(timestamp, random_value=0)
    highest = get_timestamp_random(timestamp + 1, random_value=0)
    return lowest, highest
