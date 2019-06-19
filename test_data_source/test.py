import boto3
import random
from boto3.dynamodb.conditions import Key
from datetime import datetime as dt
import json

client = boto3.resource("dynamodb")

table = client.Table("dataplattform")


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


def insert_doc(type, data=None, timestamp=None):
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

    print("Inserted")


def get_docs(type, timestamp_from=0, timestamp_to=2147483647):
    """
    :param type: Which type of documents should be fetched.
    :param timestamp_from: Start unix time. Default 0
    :param timestamp_to: end unix time. Default 2147483647
    :return: A list of all documents found.
    """
    lower_value = get_range_timestamp_random(timestamp_from)[0]
    upper_value = get_range_timestamp_random(timestamp_to)[1]

    response = table.query(
        KeyConditionExpression=Key('timestamp_random').between(lower_value, upper_value) & Key(
            'type').eq(type),
    )
    items = response['Items']
    return items


def main():
    f = open("example_data.json")
    example_data = json.loads(f.read())
    f.close()
    for example in example_data:
        insert_doc(type=example["type"], data=example["data"], timestamp=example["timestamp"])

    docs = get_docs("temp", timestamp_from=1560867713, timestamp_to=1560867903)
    for doc in docs:
        print(doc["timestamp"])


if __name__ == '__main__':
    main()
