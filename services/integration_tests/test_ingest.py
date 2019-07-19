import json
from datetime import datetime
import integration_tests_util as util

INGEST_CONFIG = util.read_serverless_output("ingest")


def test_load_config():
    assert "IngestURL" in INGEST_CONFIG
    assert "TravisIngestKey" in INGEST_CONFIG

    assert INGEST_CONFIG["IngestURL"].endswith("/")


def test_needs_apikey():
    response_code, _ = util.post_to_api("{}", INGEST_CONFIG["IngestURL"] + "whatever")
    assert response_code == 500


def test_can_post_to_ingest():
    url = INGEST_CONFIG["IngestURL"] + "YeetType"
    apikey = INGEST_CONFIG["TravisIngestKey"]
    response_code, response_body = util.post_to_api("{}", url, apikey=apikey)
    assert response_code == 200
    body = json.loads(response_body)
    assert "timestamp" in body
    timestamp = int(body["timestamp"])
    timestamp_now = int(datetime.now().timestamp())
    assert timestamp <= timestamp_now
