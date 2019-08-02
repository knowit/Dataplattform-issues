import json

import boto3
import integration_tests_util as util
from datetime import datetime as dt

import pymysql

MYSQL_CONFIG = util.read_serverless_output("structured_mysql")
INGEST_CONFIG = util.read_serverless_output("ingest")


def test_dayratingtype_batch():
    ingest_url = INGEST_CONFIG["IngestURL"] + "DayRatingType"
    ingest_apikey = INGEST_CONFIG["TravisIngestKey"]

    body = json.dumps({
        "button": -1
    })
    response_code, response_body = util.post_to_api(body, ingest_url, apikey=ingest_apikey)
    assert response_code == 200
    assert "timestamp" in response_body
    assert "id" in response_body
    timestamp = int(response_body["timestamp"])
    id = response_body["id"]
    response = invoke_batch_job("DayRatingType", timestamp_from=timestamp)
    assert response["StatusCode"] == 200

    with get_mysql_cursor() as cursor:
        sql = "SELECT * FROM DayRatingType WHERE id = %s;"
        n_results = cursor.execute(sql, [id])
        assert n_results == 1
        row = cursor.fetchone()
        assert row["timestamp"] == timestamp
        assert row["button"] == -1


def invoke_batch_job(type, timestamp_from=None, timestamp_to=None):
    if not timestamp_from:
        timestamp_from = int(dt.now().timestamp()) - 10 * 60  # 10 minutes ago
    if not timestamp_to:
        timestamp_to = int(dt.now().timestamp())

    event = {
        "types": [
            type
        ],
        "timestamp_from": timestamp_from,
        "timestamp_to": timestamp_to
    }
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName=MYSQL_CONFIG["batchJobLambda"],
        LogType='None',
        Payload=json.dumps(event).encode()
    )

    return response


def get_mysql_cursor():
    connection = pymysql.connect(
        host=MYSQL_CONFIG["auroraClusterROEndpoint"],
        port=int(MYSQL_CONFIG["auroraDBPort"]),
        user=MYSQL_CONFIG["auroraDBUser"],
        password=MYSQL_CONFIG["auroraDBPassword"],
        db=MYSQL_CONFIG["auroraDBName"],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    return connection
