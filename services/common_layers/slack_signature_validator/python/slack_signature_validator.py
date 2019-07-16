import hmac
import hashlib
import os
import json


def check_slack_event_legit(event):
    body = event["body"]
    headers = event["headers"]
    if ("X-Slack-Signature" not in headers) or ("X-Slack-Request-Timestamp" not in headers):
        return {
            'statusCode': 403,
            'body': json.dumps({"reason": "No signature"})
        }
    received_signature = headers["X-Slack-Signature"]
    slack_timestamp = headers["X-Slack-Request-Timestamp"]
    if validate_payload_signature(body, received_signature, slack_timestamp):
        return {
            'statusCode': 200,
            'body': ""
        }
    else:
        return {
            'statusCode': 403,
            'body': json.dumps({"reason": "Invalid signature"})
        }


def validate_payload_signature(body, received_signature, slack_timestamp,
                               shared_secret=os.getenv("DATAPLATTFORM_SLACK_SECRET")):
    """
    As described by https://api.slack.com/docs/verifying-requests-from-slack
    """
    # TODO fail signature if timestamp is not recent?
    basestring = ("v0:" + slack_timestamp + ":" + body).encode()
    calculated_signature = "v0=" + hmac.new(shared_secret.encode(), basestring,
                                            hashlib.sha256).hexdigest()
    return hmac.compare_digest(calculated_signature, received_signature)
