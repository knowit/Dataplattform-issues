import json
import urllib.parse
import urllib.request
import boto3
import slack_signature_validator


def lambda_handler(event, context):
    slack_validator = slack_signature_validator.check_slack_event_legit(event)
    if not slack_validator["statusCode"] == 200:
        return slack_validator

    body = event["body"]

    # parse_qs converts a http parameter list like this: token=123&param2=12 into a nice
    # dictionary.
    slack_params = urllib.parse.parse_qs(body)
    command = slack_params.get("command", [])

    if "/arrangement" in command:
        data = {
            "response_url": slack_params["response_url"][0],
            "event_type": "/event_button"
        }

        return invoke_and_return(data)

    if "/registrer-arrangement" in command:
        data = {
            "event_type": "/register",
            "response_url": slack_params["response_url"][0],
            "user_id": slack_params["user_id"][0]
        }

        return invoke_and_return(data)

    elif "payload" in slack_params:
        payload = json.loads(slack_params["payload"][0])
        payload_type = payload["type"]

        # Someone clicked on a block action
        if payload_type == "block_actions":
            action_text = payload["actions"][0]["text"]["text"]

            if action_text == "Registrer arrangement":
                event_id = payload["actions"][0]["value"]
                data = {
                    "trigger_id": payload["trigger_id"],
                    "response_url": payload["response_url"],
                    "event_id": event_id,
                    "event_type": "register_event"
                }
            # else if the payload is because a "få kode" button has been pressed.
            # TODO: don't hardcode this.
            else:
                event_id_clicked = payload["actions"][0]["value"]
                data = {
                    "response_url": payload["response_url"],
                    "event_id_clicked": event_id_clicked,
                    "event_type": "click_action",
                    "user_id": payload["user"]["id"]
                }

        # Someone submitted a dialog containing extra event information.
        elif payload["type"] == "dialog_submission":
            data = {
                "submission": payload["submission"],
                "event_type": "dialog_submission",
                "event_id": payload["state"],
                "response_url": payload["response_url"]
            }

            # In order to confirm that the dialog is complete and should be closed the
            # success_text needs to be an empty json object.
            return invoke_and_return(data, success_text="{}")

        else:
            return {
                'statusCode': 400,
                'body': "Unsupported payload type"
            }

        return invoke_and_return(data)


def invoke_and_return(data, success_text="Vi jobber med saken..."):
    """
    :param data: The data that should be sent to the invoked lambda.
    :return: Returns a status code 200 if everything is fine. And also 200 but a different text
    if the lambda was not invoked. This is because the text shows up in slack if the statuscode
    is 200.
    """
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName='dataplattform_slack_response',
        InvocationType='Event',
        LogType='None',
        ClientContext='string',
        Payload=json.dumps(data).encode()
    )

    # Invoked correctly if statuscode is 202.
    if response["StatusCode"] == 202:
        return {
            'statusCode': 200,
            'body': success_text
        }
    else:
        return {
            'statusCode': 200,
            'body': "Noe gikk galt."
        }
