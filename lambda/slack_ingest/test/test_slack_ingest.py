import slack_ingest


def test_missing_signature():
    event = {
        "body": "{}",
        "headers": {

        }
    }
    response = slack_ingest.handler(event, {})
    assert response["statusCode"] == 403
    assert "No signature" in response["body"]


