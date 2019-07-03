import json
import urllib.parse
import urllib.request
import boto3


def lambda_handler(event, context):
    body = event["body"]

    # parse_qs converts a http parameter list like this: token=123&param2=12 into a nice
    # dictionary.
    slack_params = urllib.parse.parse_qs(body)

    if "/event-button" in slack_params.get("command", []):
        data = {
            "response_url": slack_params["response_url"][0],
            "event_type": "/event_button"
        }

        return invoke_and_return(data)
    elif "payload" in slack_params:
        payload = json.loads(slack_params["payload"][0])
        event_id_clicked = payload["actions"][0]["value"]
        data = {
            "response_url": payload["response_url"],
            "event_id_clicked": event_id_clicked,
            "event_type": "click_action"
        }

        return invoke_and_return(data)


def invoke_and_return(data):
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName='dataplattform_slack_response',
        InvocationType='Event',
        LogType='None',
        ClientContext='string',
        Payload=json.dumps(data).encode()
    )

    if response["StatusCode"] == 202:
        return {
            'statusCode': 200,
            'body': "Vi jobber med saken..."
        }
    else:
        return {
            'statusCode': 200,
            'body': "Noe gikk galt."
        }
