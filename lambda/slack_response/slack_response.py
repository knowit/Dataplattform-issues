import datetime
import os
import pickle
import googleapiclient.discovery
import logging
import json
import urllib.request
import random
import boto3
from boto3.dynamodb.conditions import Key, Attr

client = boto3.resource("dynamodb")
table = client.Table("dataplattform_event_codes")


def handler(event, context):
    if not os.path.exists('token.pickle'):
        return {
            'statusCode': 500,
            'body': 'oof'
        }
    # Silence warning from google libraries
    logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    calendar_id = os.getenv("DATAPLATTFORM_FAGKALENDER_ID")
    calendar_events = get_events(creds, calendar_id)

    response_url = event["response_url"]
    event_type = event["event_type"]

    if event_type == "/event_button":
        blocks = create_blocks(calendar_events)
        send_response(blocks, response_url)
    elif event_type == "click_action":
        event_id_clicked = event["event_id_clicked"]
        now = int(datetime.datetime.now().timestamp())
        to = now + 24 * 60 * 60  # TODO
        event_name = calendar_events[event_id_clicked]["summary"]
        code = create_code(event_id_clicked, event_name, now, to)
        blocks = create_blocks(calendar_events, {event_id_clicked: code})

        send_response(blocks, response_url)

    return {
        'statusCode': 200,
        'body': {}
    }


def get_code(event_id):
    """
    :param event_id:
    :return: Returns an existing code for a specific event. Or None if it doesn't exist.
    """

    response = table.query(KeyConditionExpression=Key('event_id').eq(event_id))
    items = response["Items"]
    if items:
        return items[0]["event_code"]
    return None


def collision(code, timestamp_from, timestamp_to):
    filter_expr = Attr('event_code').eq(code) & (
            Attr('timestamp_from').lt(timestamp_to) | Attr('timestamp_to').gt(timestamp_from))
    response = table.scan(FilterExpression=filter_expr, ConsistentRead=True)
    items = response['Items']
    return len(items) > 0


def create_code(event_id, event_name, timestamp_from, timestamp_to):
    """
    :param event_id:
    :return: Returns either a new id for the calendar/ event ID or an existing one.
    """
    existing_code = get_code(event_id)
    if existing_code:
        return existing_code

    digits = 6
    event_code = random.randint(0, (2 ** digits) - 1)
    code = format(event_code, '0' + str(digits) + 'b')

    if collision(code, timestamp_from, timestamp_to):
        return create_code(event_id, event_name, timestamp_from, timestamp_to)

    table.put_item(Item={
        'event_id': event_id,
        'event_code': code,
        'event_name': event_name,
        'timestamp_from': timestamp_from,
        'timestamp_to': timestamp_to,
    })
    return code


def send_response(blocks, response_url):
    data = {
        "attachments": [
            {
                "blocks": blocks
            }
        ]

    }
    req = urllib.request.Request(response_url, data=json.dumps(data).encode())
    response = urllib.request.urlopen(req)
    return response


def create_event_section(title, date, id):
    event_code = get_code(id)
    section = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*" + title + "* \n " + date
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Få kode" if event_code is None else event_code

                },
                "value": id,
                "action_id": "button",

            }
        },
        {
            "type": "divider"
        },
    ]
    if event_code:
        section[0]["accessory"]["style"] = "primary"
    return section


def create_blocks(events, data=None):
    # TODO: remove extra. this is just for testing purposes.
    extra = ""
    if data is not None:
        extra += str(list(data.keys())[0])
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Velg arrangementet du vil bruke knappen på."
                        "\n (Listen er hentet fra google calender, lag event der først om du ikke "
                        "ser den på listen her.) (link til wiki-side på hvordan)"
            }
        },
        {
            "type": "divider"
        }
    ]

    for event_id, event_info in events.items():
        title = event_info["summary"]
        date = event_info["start"]
        id = event_id
        block = create_event_section(title, date, id)
        blocks.extend(block)
    return blocks


def get_events(creds, calendar_id):
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime') \
        .execute()
    events = events_result.get('items', [])

    info = {}
    for event in events:
        info[event['id']] = {
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'summary': event['summary'],
        }
    return info
