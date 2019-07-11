import datetime
import os
import googleapiclient.discovery
import logging
import json
import urllib.request
import urllib.parse
import random
import boto3
import httplib2
import dateutil
from boto3.dynamodb.conditions import Key, Attr
from oauth2client.service_account import ServiceAccountCredentials

client = None
table = None

GUILDS_AND_CHAPTERS = ["Web Chapter", "Ruby Guild", "Security Guild", "Hardware Guild",
                       "Kodekino", "Creative crew", "Artificial Chapter", "Rust Guild",
                       "Rådgivning & ledelse", "User Chapter", "Quality Chapter", "JVM Chapter",
                       "Architecture Chapter", "Virtual Guild", "dotnet Chapter", "Speakers Guild",
                       "Engineering Leadership Chapter"]


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
        send_response_blocks(blocks, response_url)

    # This event is when someone clicked on `få kode` on some event.
    elif event_type == "click_action":
        event_id_clicked = event["event_id_clicked"]
        calendar_event = calendar_events[event_id_clicked]
        user_id = event["user_id"]

        event_start = calendar_event['start']
        event_end = calendar_event['end']
        code_valid_from = int(datetime.datetime.now().timestamp())
        code_valid_to = int(dateutil.parser.parse(event_end).timestamp())
        # Add one day to the end timestamp.
        code_valid_to = code_valid_to + 24 * 60 * 60
        event_name = calendar_event["summary"]

        # Try to create a new code for the event just clicked.
        create_code(event_id_clicked, event_name, user_id, event_start, event_end,
                    code_valid_from, code_valid_to)
        blocks = create_blocks(calendar_events)
        send_response_blocks(blocks, response_url)

    # This event is when someone clicks the register event button in slack.
    elif event_type == "register_event":
        trigger_id = event["trigger_id"]
        event_id = event["event_id"]
        dialog = create_dialog(event_id)
        params = {
            "token": os.getenv("SLACK_BOT_TOKEN"),
            "dialog": dialog,
            "trigger_id": trigger_id
        }
        send_response("https://slack.com/api/dialog.open", params=params)

    # This is when someone submits the dialog.
    elif event_type == "dialog_submission":
        submission = event["submission"]
        number_of_people_attended = int(submission["number_of_people"])
        guild = submission["guild"]
        event_id = event["event_id"]

        status_code = save_event(event_id, number_of_people_attended, guild)
        success_code = 200 <= status_code < 300
        text = "Tusen takk for tilbakemelding!" if success_code else "Noe gikk galt, kunne ikke " \
                                                                     "lagre data."
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        ]
        send_response_blocks(blocks, response_url)

    return {
        'statusCode': 200,
        'body': {}
    }


def save_event(event_id, n_people, guild):
    """
    :param event_id: The id of the event that is going to be saved as a refined EventType.
    :param n_people: How many people attended this event.
    :param guild: Which guild was responsible for this event.
    :return: A status code after an attempt of sending this event to the ingest API.
    """
    event = get_event(event_id)
    body = {
        "event_id": event_id,
        "event_name": event["event_name"],
        "event_start": event["event_start"],
        "event_end": event["event_end"],
        "number_of_people": n_people,
        "guild": guild
    }

    ingest_url = os.getenv("DATAPLATTFORM_INGEST_URL")
    apikey = os.getenv("DATAPLATTFORM_INGEST_APIKEY")
    data = json.dumps(body).encode()
    try:
        request = urllib.request.Request(ingest_url, data=data, headers={"x-api-key": apikey})
        response = urllib.request.urlopen(request)
        return response.getcode()
    except urllib.request.HTTPError:
        return 500


def create_dialog(event_id):
    options = [{"label": guild, "value": guild} for guild in GUILDS_AND_CHAPTERS]
    # In case this event was not for any guild it's good to have an option for other.
    options.append({
        "label": "Annen/ ingen",
        "value": "Annen/ ingen"
    })

    select = {
        "label": "Hvilken faggruppe?",
        "type": "select",
        "name": "guild",
        "options": options
    }

    # TODO: should this fetch the number of people who voted on this event as an estimate for
    #  how many people came?
    dialog = {
        "callback_id": event_id,
        "title": "Arrangement",
        "state": event_id,
        "elements": [
            {
                "label": "Hvor mange kom på arrangementet?",
                "name": "number_of_people",
                "type": "text",
                "subtype": "number",
                "placeholder": 100
            },
            select
        ]
    }
    return dialog


def get_event(event_id):
    """
    :param event_id:
    :return: Returns an existing event for a specific event. Or None if it doesn't exist.
    """
    response = table.query(KeyConditionExpression=Key('event_id').eq(event_id))
    items = response["Items"]
    if items:
        return items[0]
    return None


def get_code(event_id):
    """
    :param event_id:
    :return: Returns an existing code for a specific event. Or None if it doesn't exist.
    """
    event = get_event(event_id)
    if event:
        return event["event_code"]
    return None


def collision(event_code, code_valid_from, code_valid_to):
    """
    :param event_code: Which event_code you want to check for collision. Example: 010111
    :param code_valid_from: In which range do you want to check for this specific event_code.
    :param code_valid_to: End of the timeslot range.
    :return: Returns True if there already is another event_code active for this time frame.
    False if there is no other and it is safe to use.
    """
    filter_expr = Attr('event_code').eq(event_code) & (
            Attr('code_valid_from').lt(code_valid_to) | Attr('code_valid_to').gt(code_valid_from))
    response = table.scan(FilterExpression=filter_expr, ConsistentRead=True)
    items = response['Items']
    return len(items) > 0


def create_code(event_id, event_name, user_id, event_start, event_end, code_valid_from,
                code_valid_to):
    """
    :param event_id: the event_id fetched from google calendar.
    :param event_name: The name of the event.
    :param event_start: When the event starts.
    :param event_end: When the event ends.
    :param code_valid_from: When the code is valid and should be used, timestamp.
    :param code_valid_to: When the code is valid and should be used, timestamp.
    :return: Returns either a new id for the calendar/ event ID or an existing one.
    """
    existing_code = get_code(event_id)
    if existing_code:
        return existing_code

    # How many digits the event_code should be.
    digits = 6
    random_code = random.randint(0, (2 ** digits) - 1)
    event_code = format(random_code, '0' + str(digits) + 'b')

    if collision(event_code, code_valid_from, code_valid_to):
        # If there is a collision for this specific event_code then we retry.
        return create_code(event_id, event_name, user_id, code_valid_from, code_valid_to)

    table.put_item(Item={
        'event_id': event_id,
        'event_code': event_code,
        'event_name': event_name,
        'event_start': event_start,
        'event_end': event_end,
        'code_valid_from': code_valid_from,
        'code_valid_to': code_valid_to,
    })
    # TODO: maybe the scheduled IM should be a bit later then just right after the event is done.
    send_scheduled_im(event_name, user_id, event_id, code_valid_to)
    return event_code


def send_scheduled_im(event_name, user_id, event_id, timestamp):
    """
    This method schedules an IM to the user that created the event_code. The message can contain
    follow up questions about the event. For instance: how many people came to the event. etc.
    :param event_name: Which event this scheduled IM is about.
    :param user_id: Which user should this IM be sent to.
    :param event_id: which event this IM is a response to.
    :param timestamp: At what time should this IM be sent.
    :return: True if successful.
    """

    message = f"Hei \nHåper {event_name} var vellykket. \nFor å få litt mer informasjon om " \
        f"dette arrangementet er det fint om du svarer på noen spørsmål angående arrangementet. "

    attachments = [
        {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Registrer arrangement"
                            },
                            "style": "primary",
                            "value": event_id
                        }
                    ]
                }
            ]
        }
    ]

    params = {
        "token": os.getenv("SLACK_BOT_TOKEN"),
        "channel": user_id,
        "as_user": True,
        "post_at": timestamp,
        "attachments": json.dumps(attachments)
    }
    base_url = "https://slack.com/api/chat.scheduleMessage"
    return send_response(base_url, params=params)


def send_response_blocks(blocks, response_url):
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
    return send_response(response_url, data=data)


def send_response(response_url, data=None, params=None):
    """
    :param data: data to be sent. (dictionary)
    :param response_url: The Slack hook response_url. AKA where the data should be sent back.
    :param params: Extra http parameters if needed.
    :return: The urllib response
    """
    if params:
        query = urllib.parse.urlencode(params)
        response_url = response_url + "?" + query

    if data:
        req = urllib.request.Request(response_url, data=json.dumps(data).encode())
    else:
        req = urllib.request.Request(response_url)
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
                "action_id": "button"
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
                        "ser den på listen her.)\n Les hvordan du kobler opp her: \n "
                        "https://github.com/knowit/Dataplattform/wiki/Lage-et-arrangement-koblet-opp-mot-vurderingssystemet"
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
            'end': event['end'].get('dateTime', event['end'].get('date')),
            'summary': event['summary'],
        }
    return info
