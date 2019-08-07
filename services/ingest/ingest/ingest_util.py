import timestamp_random as tr
from datetime import datetime as dt
import boto3
import os


class IngestUtil:
    __table = None

    @staticmethod
    def get_table():
        if IngestUtil.__table is None:
            client = boto3.resource("dynamodb")
            table_name = os.getenv("DATAPLATTFORM_RAW_TABLENAME")
            table = client.Table(table_name)
            IngestUtil.__table = table
        return IngestUtil.__table

    @staticmethod
    def insert_doc(type, data=None, timestamp=None):
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

        IngestUtil.get_table().put_item(
            Item=item
        )

        return timestamp, timestamp_random
