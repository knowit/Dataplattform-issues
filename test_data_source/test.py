import boto3
import random
from boto3.dynamodb.conditions import Key

from datetime import datetime as dt


def get_random_timestamp():
    def to_byte_array(number: int, bytes: int):
        return number.to_bytes(bytes, 'big')

    time = int(dt.now().timestamp())
    return to_byte_array((time << 64) + random.getrandbits(64), 16)


client = boto3.resource("dynamodb")

table = client.Table("dataplattform")
time = int(dt.now().timestamp())
table.put_item(
    Item={
        "type": "temp",
        "timestamp_random": get_random_timestamp(),
        "data": {
            "haw": "yee"
        },
        "timestamp": time
    }
)

print("Inserted")

response = table.query(
    KeyConditionExpression=Key('timestamp_random').lt(get_random_timestamp()) & Key('type').eq("temp"),
)
items = response['Items']
# print(items)
for i in items:
    print(i)
    if 'timestamp' in i:
        print(int(i['timestamp']))
