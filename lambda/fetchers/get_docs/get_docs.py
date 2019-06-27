import boto3
from boto3.dynamodb.conditions import Key
import json
import base64
import timestamp_random as tr


def handler(event, context):
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
        doc["id"] = base64.b64encode(doc["timestamp_random"].value).decode("utf-8")
        del doc["timestamp_random"]
        doc["timestamp"] = int(doc["timestamp"])
        if "data" in doc:
            doc["data"] = json.loads(doc["data"])
        else:
            doc["data"] = {}
    return docs


def get_docs(table, data_type, timestamp_from, timestamp_to):
    """
    :param table: DynamoDB table.
    :param data_type: Which type of documents should be fetched.
    :param timestamp_from: Start unix time.
    :param timestamp_to: end unix time.
    :return: A list of all documents found.
    """
    lower_value = tr.get_range_timestamp_random(timestamp_from)[0]
    upper_value = tr.get_range_timestamp_random(timestamp_to)[1]

    response = table.query(
        KeyConditionExpression=Key('timestamp_random').between(lower_value, upper_value) & Key(
            'type').eq(data_type),
    )
    items = response['Items']
    return items
