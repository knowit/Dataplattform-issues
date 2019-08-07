import base64
import json
from ingest.ingest_util import IngestUtil
import ingest.filters as filters


def handler(event, context):
    data_type = event["pathParameters"]["type"]
    data = (event["body"])
    if data_type in filters.filter:
        data = filters.filter[data_type](data)
    timestamp, timestamp_random = IngestUtil.insert_doc(data_type, data=data)
    return {
        'statusCode': 200,
        'body': json.dumps({
            "timestamp": timestamp,
            "id": base64.b64encode(timestamp_random).decode("utf-8")
        })
    }
