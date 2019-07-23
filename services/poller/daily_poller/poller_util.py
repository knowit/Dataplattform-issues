import boto3
from boto3.dynamodb.conditions import Key
import json
import os
import urllib.request

client = None
table = None


def set_global_client_table():
    """
    A method that sets the global variables table and client.
    TODO: This is quite bad practice and we should use just a simple class instead of this.
    """
    global client
    global table

    if client is None or table is None:
        client = boto3.resource("dynamodb")
        table = client.Table(os.getenv("DATAPLATTFORM_POLLING_STATUS_TABLENAME"))


def upload_last_inserted_doc(last_inserted_doc, type):
    """
    This method simply inserts the last_inserted_doc's reg_period into a table.
    :param last_inserted_doc: The document that is going to be uploaded.
    :param type: Which type this is.
    :return: Nothing
    """
    set_global_client_table()
    table.put_item(Item={
        'type': type,
        'last_inserted_doc': last_inserted_doc
    })


def fetch_last_inserted_doc(type):
    """
    This method fetches the last_inserted_doc from the DynamoDB table and returns the
    last_inserted_doc.
    :param type: Which type.
    :return: last_inserted_doc. or None if there was nothing saved.
    """
    set_global_client_table()
    response = table.query(KeyConditionExpression=Key('type').eq(type))
    items = response["Items"]
    if items:
        return items[0]["last_inserted_doc"]
    return None


def post_to_ingest_api(data, type):
    """
    This method uploads data to the ingest API.
    :param data: the data you want to send, as a dictionary.
    :return: a status code.
    """
    ingest_url = os.getenv("DATAPLATTFORM_INGEST_URL") + type
    apikey = os.getenv("DATAPLATTFORM_INGEST_APIKEY")
    data = json.dumps(data).encode()
    try:
        request = urllib.request.Request(ingest_url, data=data, headers={"x-api-key": apikey})
        response = urllib.request.urlopen(request)
        return response.getcode()
    except urllib.request.HTTPError:
        return 500
