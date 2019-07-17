import os

import boto3
from boto3.dynamodb.conditions import Key
from data_types.AbstractType import AbstractType

# Map event_code -> [event objects] (several events may share event code)
events_cache = {}


def get_events(event_code):
    if event_code not in events_cache:
        fetch_events(event_code)
    return events_cache[event_code]


def fetch_events(event_code):
    client = boto3.resource("dynamodb")
    table_name = os.getenv("DATAPLATTFORM_EVENT_CODE_TABLE")
    table = client.Table(table_name)

    key_expression = Key('event_code').eq(event_code)

    response = table.scan(FilterExpression=key_expression)
    items = response['Items']

    while response.get('LastEvaluatedKey'):
        response = table.scan(FilterExpression=key_expression,
                              ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    events_cache[event_code] = items


def get_event(event_code, timestamp):
    """Get the event to match with an event rating"""
    events = get_events(event_code)
    for event in events:
        ts_from = event["code_valid_from"]
        ts_to = event["code_valid_to"]
        if ts_from < timestamp < ts_to:
            return event
    return None


def get_event_name(doc):
    data = doc["data"]
    if "event_code" not in data:
        return None
    event_code = data["event_code"]
    timestamp = doc["timestamp"]
    event = get_event(event_code, timestamp)
    if event:
        return event.get("event_name")
    return None


class EventRatingType(AbstractType):
    attributes_keep = {
        ("button", int): ["data", "button"],
        ("event_name", str, get_event_name): [],
    }

    def accept_row(self, row):
        """Ignore rating events that cannot be linked to an event"""
        return row["event_name"] is not None
