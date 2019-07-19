import integration_tests_util as util

FETCH_CONFIG = util.read_serverless_output("fetch")


def test_load_config():
    assert "GetDocsURL" in FETCH_CONFIG
    assert "TravisFetchApiKey" in FETCH_CONFIG

    assert FETCH_CONFIG["GetDocsURL"].endswith("/")
