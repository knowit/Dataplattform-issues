import json
from ingest.ingest_util import IngestUtil
import re


def filter_github(data):
    data_dict = json.loads(data)
    if data_dict.get("repository") and data_dict["repository"].get("private"):
        return None
    return data


def remove_emoji_modifiers(reaction):
    if "::skin-tone-" in reaction:
        reaction = re.sub(r'::skin-tone-.', '', reaction)
    return reaction


def analyze_slack_messages(slack_message, channel, event_time, team_id):
    """
    :param slack_message: The slack message (str)
    :param channel: Slack channel id.
    :param event_time: slack event_time.
    :param team_id: Slack team id.
    :return: A list of documents that should be added
    """
    slack_message = remove_emoji_modifiers(slack_message)

    reactions = []
    # For cases where you type multiple emojis with no space inbetween them.
    if "::" in slack_message:
        slack_message = slack_message.replace("::", ": :")

    for word in slack_message.split():
        if word.startswith(":") and word.endswith(":"):
            reaction = word[1:-1]
            reactions.append(reaction)
    documents = []
    for reaction in reactions:
        document = {
            "event": {
                "type": "reaction_added",  # TODO: Should this be a different type?
                "item": {
                    "channel": channel
                },
                "reaction": reaction
            },
            "event_time": event_time,
            "team_id": team_id,
        }
        documents.append(json.dumps(document))
    return documents


def filter_slack(data):
    # Being very careful to only select the data points we need as to not accidentally include some
    # personal information
    data_dict = json.loads(data)
    if "event" not in data_dict:
        return None

    channel = data_dict["event"]["channel"]
    event_time = data_dict["event_time"]
    team_id = data_dict["team_id"]
    if "text" in data_dict["event"]:
        slack_message = data_dict["event"]["text"]
        documents = analyze_slack_messages(slack_message, channel, event_time, team_id)
        for document in documents:
            IngestUtil.insert_doc("SlackEmojiType", document)
    document = {
        "event": {
            "type": "message",
            "channel": channel
        },
        "event_time": event_time,
        "team_id": team_id,
    }

    return json.dumps(document)


def filter_slack_reaction(data):
    # Being very careful to only select the data points we need as to not accidentally include some
    # personal information
    data_dict = json.loads(data)
    if "event" not in data_dict:
        return None
    channel = data_dict["event"]["item"]["channel"]
    if not channel.startswith("C"):
        # Drop the data point if message was not in a public channel
        return None
    reaction = remove_emoji_modifiers(data_dict["event"]["reaction"])
    document = {
        "event": {
            "type": "reaction_added",
            "item": {
                "channel": channel
            },
            "reaction": reaction
        },
        "event_time": data_dict["event_time"],
        "team_id": data_dict["team_id"],
    }

    return json.dumps(document)


"""
Map of optional filter functions for data types. Value is a function that returns a redacted
version of the data point, or None if the data point should be ignored.
"""
filter = {
    "GithubType": filter_github,
    "SlackType": filter_slack,
    "SlackReactionType": filter_slack_reaction
}
