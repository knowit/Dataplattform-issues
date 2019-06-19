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
    example output is [AAAAAF0I83cAAAAAAAAAAA==,
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


def main():
    f = open("example_data.json")
    example_data = json.loads(f.read())
    f.close()
    for example in example_data:
        insert_doc(type=example["type"], data=example["data"], timestamp=example["timestamp"])

    response = table.query(
        KeyConditionExpression=Key('timestamp_random').lt(get_timestamp_random()) & Key('type').eq(
            "temp"),
    )
    items = response['Items']
    # print(items)
    for i in items:
        print(i)
        if 'timestamp' in i:
            print(int(i['timestamp']))


if __name__ == '__main__':
    main()
