import integration_tests_util as util

FETCH_CONFIG = util.read_serverless_output("fetch")


def test_load_config():
    assert "GetDocsURL" in FETCH_CONFIG
    assert "TravisFetchApiKey" in FETCH_CONFIG

    assert FETCH_CONFIG["GetDocsURL"].endswith("/")


def test_can_fetch_with_apikey():
    fetch_url = FETCH_CONFIG["GetDocsURL"] + "SomeTestingType"
    fetch_apikey = FETCH_CONFIG["TravisFetchApiKey"]

    response_code, response_body = util.get_from_api(fetch_url, apikey=fetch_apikey)
    assert response_code == 200

    assert "all_docs_url" in response_body
    assert "most_recent_25_docs" in response_body

    recent_list = response_body["most_recent_25_docs"]
    assert type(recent_list) == list

    all_docs_url = response_body["all_docs_url"]
    response_code, response_body = util.get_from_api(all_docs_url)
    assert response_code == 200
    assert type(response_body) == list
    # The total list from the all_docs_url should be at least as long as the recent_doc list
    assert len(response_body) >= len(recent_list)


def test_cannot_fetch_without_apikey():
    fetch_url = FETCH_CONFIG["GetDocsURL"] + "SomeTestingType"

    response_code, response_body = util.get_from_api(fetch_url)
    assert response_code == 500


def test_cannot_fetch_with_wrong_apikey():
    fetch_url = FETCH_CONFIG["GetDocsURL"] + "SomeTestingType"

    response_code, response_body = util.get_from_api(fetch_url,
                                                     apikey="randomstringhopethiswillneverwork")
    assert response_code == 500
