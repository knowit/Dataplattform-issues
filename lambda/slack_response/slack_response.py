import datetime
import os
import pickle
import googleapiclient.discovery
import logging


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

    # TODO insert into slack response
    info = get_events(creds, calendar_id)

    return {
        'statusCode': 200,
        'body': info
    }


def get_events(creds, calendar_id):
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=calendar_id,
        # calendarId='primary',
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
            'summary': event['summary']
        }
        info.append(i)
    return info
