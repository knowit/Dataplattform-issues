import json
import urllib.request
from datetime import datetime

import pytest

ingest_config = None
ingest_url = None
ingest_apikey = None


@pytest.fixture(scope="session", autouse=True)
def load_configs():
    ingest = read_serverless_output("ingest")
    assert "IngestURL" in ingest
    assert "TravisIngestKey" in ingest

    global ingest_config
    global ingest_url
    global ingest_apikey
    ingest_config = ingest
    ingest_url = ingest_config["IngestURL"]
    ingest_apikey = ingest_config["TravisIngestKey"]

    assert ingest_url.endswith("/")


# TODO extract this to a shared module for all tests?
def read_serverless_output(service):
    f = open(f"{service}.serverless_outputs.json")
    data = json.loads(f.read())
    f.close()
    return data


# TODO generalize and extract to shared module?
def post_to_ingest_api(body, url, apikey=None) -> (int, str):
    data = body.encode("ascii")
    headers = {"x-api-key": apikey} if apikey else {}
    try:
        request = urllib.request.Request(url, data=data, headers=headers)
        response = urllib.request.urlopen(request)
        return response.getcode(), response.read().decode()
    except urllib.request.HTTPError:
        return 500, None


def test_needs_apikey():
    response_code, _ = post_to_ingest_api("{}", ingest_url + "whatever")
    assert response_code == 500


def test_can_post_to_ingest():
    url = ingest_url + "YeetType"
    response_code, response_body = post_to_ingest_api("{}", url, apikey=ingest_apikey)
    assert response_code == 200
    body = json.loads(response_body)
    assert "timestamp" in body
    timestamp = int(body["timestamp"])
    timestamp_now = int(datetime.now().timestamp())
    assert timestamp <= timestamp_now
