import datetime
import os
import googleapiclient.discovery
import logging
import json
import urllib.request
import random
import boto3
import httplib2
from boto3.dynamodb.conditions import Key, Attr
from oauth2client.service_account import ServiceAccountCredentials

client = None
table = None


def handler(event, context):
    creds_file = 'creds.json'
    if not os.path.exists(creds_file):
        return {
            'statusCode': 500,
            'body': 'oof'
        }
    global client
    global table
    client = boto3.resource("dynamodb")
    table = client.Table("dataplattform_event_codes")

    # Silence warning from google libraries
    logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

    calendar_id = os.getenv("DATAPLATTFORM_FAGKALENDER_ID")
    calendar_events = get_events(creds_file, calendar_id)

    response_url = event["response_url"]
    event_type = event["event_type"]

    # This event is when someone typed in /arrangement in slack.
    if event_type == "/event_button":
        blocks = create_blocks(calendar_events)
        send_response(blocks, response_url)
    # This event is when someone clicked on `få kode` on some event.
    elif event_type == "click_action":
        event_id_clicked = event["event_id_clicked"]
        now = int(datetime.datetime.now().timestamp())
        to = now + 24 * 60 * 60  # TODO
        event_name = calendar_events[event_id_clicked]["summary"]
        # Try to create a new code for the event just clicked.
        create_code(event_id_clicked, event_name, now, to)
        blocks = create_blocks(calendar_events)
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


def collision(event_code, timestamp_from, timestamp_to):
    """
    :param event_code: Which event_code you want to check for collision. Example: 010111
    :param timestamp_from: In which range do you want to check for this specific event_code.
    :param timestamp_to: End of the timeslot range.
    :return: Returns True if there already is another event_code active for this time frame.
    False if there is no other and it is safe to use.
    """
    filter_expr = Attr('event_code').eq(event_code) & (
            Attr('timestamp_from').lt(timestamp_to) | Attr('timestamp_to').gt(timestamp_from))
    response = table.scan(FilterExpression=filter_expr, ConsistentRead=True)
    items = response['Items']
    return len(items) > 0


def create_code(event_id, event_name, timestamp_from, timestamp_to):
    """
    :param event_id: the event_id fetched from google calendar.
    :param event_name: The name of the event.
    :param timestamp_from: When the event starts.
    :param timestamp_to: When the event ends.
    :return: Returns either a new id for the calendar/ event ID or an existing one.
    """
    existing_code = get_code(event_id)
    if existing_code:
        return existing_code

    # How many digits the event_code should be.
    digits = 6
    random_code = random.randint(0, (2 ** digits) - 1)
    event_code = format(random_code, '0' + str(digits) + 'b')

    if collision(event_code, timestamp_from, timestamp_to):
        # If there is a collision for this specific event_code then we retry.
        return create_code(event_id, event_name, timestamp_from, timestamp_to)

    table.put_item(Item={
        'event_id': event_id,
        'event_code': event_code,
        'event_name': event_name,
        'timestamp_from': timestamp_from,
        'timestamp_to': timestamp_to,
    })
    return event_code


def send_response(blocks, response_url):
    """
    :param blocks: All the Slack responsive block structure. (formatted as a dictionary)
    :param response_url: The Slack hook response_url. AKA where the data should be sent back.
    :return: The urllib response
    """
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
    """
    :param title: the title for this event.
    :param date: the date for this event.
    :param id: the unique event id for this event.
    :return: a dictionary containing the slack app event section.
    """
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


def create_blocks(events):
    """
    :param events: Which events should be made into a visual Slack interactive blocks app.
    :return: the dictionary containing the whole slack interactive block app.
    """
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


def get_events(credsfile, calendar_id):
    """
    :param creds: credentials
    :param calendar_id:
    :return: A dictionary containing (max 10) of the events in the nearest future from this
    specific calendar_id.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credsfile, [
        'https://www.googleapis.com/auth/calendar.readonly'])

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = googleapiclient.discovery.build(serviceName='calendar', version='v3', http=http)

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
