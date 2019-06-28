import json
import os
import hashlib
import hmac
import urllib.request
import urllib.parse


def handler(event, context):
    body = event["body"]
    headers = event["headers"]
    if "X-Slack-Signature" not in headers:
        return {
            'statusCode': 403,
            'body': json.dumps({"reason": "No signature"})
        }
    received_signature = headers["X-Slack-Signature"]
    slack_timestamp = headers["X-Slack-Request-Timestamp"]
    if validate_payload_signature(body, received_signature, slack_timestamp):
        response = post_to_ingest_api(body)
        return {
            'statusCode': response,
            'body': ""
        }
    else:
        return {
            'statusCode': 403,
            'body': json.dumps({"reason": "Invalid signature"})
        }


def post_to_ingest_api(body):
    ingest_url = os.getenv("DATAPLATTFORM_INGEST_URL")
    apikey = os.getenv("DATAPLATTFORM_INGEST_APIKEY")
    data = body.encode("ascii")
    try:
        request = urllib.request.Request(ingest_url, data=data, headers={"x-api-key": apikey})
        response = urllib.request.urlopen(request)
        return response.getcode()
    except urllib.request.HTTPError:
        return 500


def validate_payload_signature(body, received_signature, slack_timestamp):
    """
    As described by https://api.slack.com/docs/verifying-requests-from-slack
    """
    # TODO fail signature if timestamp is not recent?
    basestring = ("v0:" + slack_timestamp + ":" + body).encode()
    shared_secret = os.getenv("DATAPLATTFORM_SLACK_SECRET")
    calculated_signature = "v0=" + hmac.new(shared_secret.encode(), basestring,
                                            hashlib.sha256).hexdigest()
    return hmac.compare_digest(calculated_signature, received_signature)
