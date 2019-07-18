import json

ingest_config = None


# Todo use fixtures here.
def load_configs():
    ingest = read_ingest_serverless_output()
    global ingest_config
    ingest_config = ingest


def read_ingest_serverless_output():
    f = open("ingest.serverless_outputs.json")
    data = json.loads(f.read())
    f.close()
    return data


def test_ingest_posts():
    assert 1 == 1
    ingest = read_ingest_serverless_output()
    assert "IngestURL" in ingest
