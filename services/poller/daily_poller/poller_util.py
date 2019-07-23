import boto3
from boto3.dynamodb.conditions import Key
import json
import os
import urllib.request


class PollerUtil:
    __table = None
    __client = None

    @staticmethod
    def get_table():
        if PollerUtil.__table is None:
            PollerUtil()
        return PollerUtil.__table

    @staticmethod
    def get_client():
        if PollerUtil.__client is None:
            PollerUtil()
        return PollerUtil.__client

    def __init__(self):
        """ Virtually private constructor. """
        if PollerUtil.__table is not None and PollerUtil.__client is not None:
            raise Exception("This class should only be created once.")
        else:
            client = boto3.resource("dynamodb")
            table = client.Table(os.getenv("DATAPLATTFORM_POLLING_STATUS_TABLENAME"))
            PollerUtil.__client = client
            PollerUtil.__table = table

    @staticmethod
    def upload_last_inserted_doc(last_inserted_doc, type):
        """
        This method simply inserts the last_inserted_doc's reg_period into a table.
        :param last_inserted_doc: The document that is going to be uploaded.
        :param type: Which type this is.
        :return: Nothing
        """
        PollerUtil.get_table().put_item(Item={
            'type': type,
            'last_inserted_doc': last_inserted_doc
        })

    @staticmethod
    def fetch_last_inserted_doc(type):
        """
        This method fetches the last_inserted_doc from the DynamoDB table and returns the
        last_inserted_doc.
        :param type: Which type.
        :return: last_inserted_doc. or None if there was nothing saved.
        """
        response = PollerUtil.get_table().query(KeyConditionExpression=Key('type').eq(type))
        items = response["Items"]
        if items:
            return items[0]["last_inserted_doc"]
        return None

    @staticmethod
    def post_to_ingest_api(data, type):
        """
        This method uploads data to the ingest API.
        :param data: the data you want to send, as a dictionary.
        :param type: Which data type.
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
