import integration_tests_util as util
import json
import random
import string
from datetime import datetime

INGEST_CONFIG = util.read_serverless_output("ingest")
FETCH_CONFIG = util.read_serverless_output("fetch")


def generate_random_string(length=10):
    random_string = ""
    for i in range(length):
        char = random.choice(string.ascii_lowercase)
        random_string += char
    return random_string


def test_ingest_doc_and_get_docs():
    # This test uploads a document with a random body into a random type and then uses get_docs in
    # order to find the document again.
    random_type = generate_random_string() + "Type"
    ingest_url = INGEST_CONFIG["IngestURL"] + random_type
    ingest_apikey = INGEST_CONFIG["TravisIngestKey"]

    random_body = {
        "random": generate_random_string(20)
    }
    response_code, response_body = util.post_to_api(json.dumps(random_body), ingest_url,
                                                    apikey=ingest_apikey)
    assert response_code == 200
    assert "timestamp" in response_body
    timestamp = int(response_body["timestamp"])
    timestamp_now = int(datetime.now().timestamp())
    assert timestamp <= timestamp_now

    # Now try to fetch the same record using get_docs.
    fetch_url = FETCH_CONFIG["GetDocsURL"] + random_type
    fetch_apikey = FETCH_CONFIG["TravisFetchApiKey"]

    response_code, response_body = util.get_from_api(fetch_url, apikey=fetch_apikey)
    assert response_code == 200
    assert "all_docs_url" in response_body
    assert "most_recent_25_docs" in response_body
    recent_docs = response_body["most_recent_25_docs"]

    # You should get 1 document back at least.
    number_of_recent_docs = len(recent_docs)
    assert number_of_recent_docs >= 1
    assert find_doc(recent_docs, random_body)
    all_docs_url = response_body["all_docs_url"]

    # Now check that the all_docs_url is also working and giving out the correct document.
    response_code, response_body = util.get_from_api(all_docs_url)
    assert response_code == 200

    number_of_docs_total = len(response_body)
    assert number_of_docs_total >= 0

    # You should get atleast as many as the number of recent docs you just got.
    assert number_of_docs_total >= number_of_recent_docs

    assert find_doc(response_body, random_body)


def find_doc(docs, body):
    """
    :param docs: a list of documents.
    :param body: the body that should be check against the docs body in order to evaluate
    similarity.
    :return: True if the body was found in one of the docs, false if not.
    """
    for doc in docs:
        # Look for the document that was just uploaded.
        if doc["data"] == body:
            return True
    return False
