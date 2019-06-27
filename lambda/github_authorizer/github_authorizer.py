import json
import os
import hashlib
import hmac
import urllib.request
import urllib.parse


def handler(event, context):
    body = event["body"]
    headers = event["headers"]
    if "X-Hub-Signature" not in headers:
        return {
            'statusCode': 403,
            'body': json.dumps({"reason": "No signature"})
        }
    received_signature = headers["X-Hub-Signature"]
    if validate_payload_signature(body, received_signature):
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


def validate_payload_signature(body, received_signature):
    rec_sig = received_signature.split("=")
    if rec_sig[0] != "sha1":
        return False
    shared_secret = os.getenv("DATAPLATTFORM_GITHUB_SECRET")
    calculated_signature = hmac.new(shared_secret.encode(), body.encode(),
                                    hashlib.sha1).hexdigest()
    return hmac.compare_digest(calculated_signature, rec_sig[1])
