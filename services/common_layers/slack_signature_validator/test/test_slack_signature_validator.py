import slack_signature_validator


def test_valid_signature():
    body = '{"body": 1}'
    timestamp = "12341234"
    shared_secret = "asdfasdfasdf"
    signature = "v0=5ebdb4d8c6f634bc7ce9449758e4ccefc82777656e817e31efadc68e67055ada"

    valid = slack_signature_validator.validate_payload_signature(body, signature, timestamp,
                                                                 shared_secret=shared_secret)
    assert valid


def test_empty_signature():
    body = '{"body": 1}'
    timestamp = "12341234"
    shared_secret = "asdfasdfasdf"
    signature = ""

    valid = slack_signature_validator.validate_payload_signature(body, signature, timestamp,
                                                                 shared_secret=shared_secret)
    assert not valid


def test_invalid_signature():
    body = '{"body": 100}'
    timestamp = "12341234"
    shared_secret = "asdfasdfasdf"
    signature = "v0=5ebdb4d8c6f634bc7ce9449758e4ccefc82777656e817e31efadc68e67055ada"

    valid = slack_signature_validator.validate_payload_signature(body, signature, timestamp,
                                                                 shared_secret=shared_secret)
    assert not valid
