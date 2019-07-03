import datetime
import os
import pickle
import googleapiclient.discovery
import logging
import json
import urllib.request


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

    # Fix slack response.

    response_url = event["response_url"]
    event_type = event["event_type"]

    if event_type == "/event_button":
        blocks = create_blocks(calendar_events)
        send_response(blocks, response_url)
    elif event_type == "click_action":
        event_id_clicked = event["event_id_clicked"]
        code = create_code(event_id_clicked)
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

    # TODO lookup from db.
    return None


def create_code(event_id):
    """
    :param event_id:
    :return: Returns either a new id for the calendar/ event ID or an existing one.
    """

    # TODO: lookup from db.
    # if not exists already.. random
    return "00010111"


def send_response(blocks, response_url):
    data = {
        "attachments": [
            {
                "blocks": blocks
            }
        ]

    }
    req = urllib.request.Request(response_url, data=json.dumps(data).encode("ascii"))
    response = urllib.request.urlopen(req)
    return response


def create_event_section(title, date, id):
    event_code = get_code(id)

    return [
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
                "style": "primary" if event_code is None else "default"
            }
        },
        {
            "type": "divider"
        },
    ]


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
                        "ser den på listen her.) (link til wiki-side på hvordan)" + extra
            }
        },
        {
            "type": "divider"
        }
    ]

    for event in events:
        title = event["summary"]
        date = event["start"]
        id = event["id"]
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

    info = []
    for event in events:
        i = {
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'summary': event['summary'],
            'id': event['id']
        }
        info.append(i)
    return info
