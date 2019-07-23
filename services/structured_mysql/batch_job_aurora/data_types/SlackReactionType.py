from data_types.AbstractType import AbstractType
from data_types.slack_util import *


def match_slack_channel(doc):
    """
    :param doc: The slack event dictionary.
    :return: the channel name of an event.
    """
    channel_id = doc["data"]["event"]["item"]["channel"]
    return get_slack_channel_name(channel_id)


class SlackReactionType(AbstractType):
    attributes_keep = {
        ("event_type", str): ["data", "event", "type"],
        ("slack_timestamp", int): ["data", "event_time"],
        ("team_id", str): ["data", "team_id"],
        ("reaction", str): ["data", "event", "reaction"],
        ("channel_name", str, match_slack_channel): []
    }
