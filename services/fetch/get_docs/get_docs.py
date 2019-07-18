import os

import boto3
from boto3.dynamodb.conditions import Key
import json
import base64
import timestamp_random as tr
import uuid


def handler(event, context):
    client = boto3.resource("dynamodb")
    table_name = os.getenv("DATAPLATTFORM_RAW_TABLENAME")
    table = client.Table(table_name)

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
    url = upload_data_to_bucket(docs)
    body = format_response(docs, url)
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': body
    }


def format_response(docs, url, n=25):
    """
    :param docs: All the raw documents sorted.
    :param url: The presigned URL containing all the documents.
    :param n: The number of recent documents that should be returned in addition to the url.
    :return: the body, formatted as a json string.
    """
    # Invert the list and slice the most n recent ones.
    most_recent_docs = docs[:-(n + 1):-1]
    return json.dumps({
        "all_docs_url": url,
        "most_recent_25_docs": most_recent_docs
    })


def docs_to_json(docs):
    """
    :param docs: raw docs from DynamoDB
    :return: Convert boto types to regular ints and strings and then parse every doc to json.
    """
    json_docs = []
    for doc in docs:
        json_doc = {
            "id": base64.b64encode(doc["timestamp_random"].value).decode("utf-8"),
            "timestamp": int(doc["timestamp"]),
            "type": doc["type"]
        }
        if "data" in doc:
            try:
                json_doc["data"] = json.loads(doc["data"])
            except json.JSONDecodeError:
                continue
        else:
            json_doc["data"] = {}
        json_docs.append(json_doc)
    return json_docs


def upload_data_to_bucket(data, bucket_name="dataplattform-get-docs-cache"):
    """
    Uploads the data and creates a presigned url that works for 5 minutes.
    :param data: the data that should be uploaded. as a dictionary.
    :param bucket_name: The name of the bucket.
    :return: The presigned url that works for 5 minutes.
    """
    data_encoded = json.dumps(data).encode(encoding='UTF-8')
    # Generate a random S3 key name
    upload_key = uuid.uuid4().hex

    s3_resource = boto3.resource("s3")
    s3_resource.Bucket(bucket_name).put_object(Key=upload_key, Body=data_encoded)

    s3_client = boto3.client('s3')
    # Generate the presigned URL for put requests
    presigned_url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': upload_key
        },
        ExpiresIn=300
    )
    return presigned_url


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

    key_expression = Key('type').eq(data_type) & Key('timestamp_random').between(lower_value,
                                                                                 upper_value)

    response = table.query(KeyConditionExpression=key_expression)
    items = response['Items']

    while response.get('LastEvaluatedKey'):
        response = table.query(KeyConditionExpression=key_expression,
                               ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    return items
