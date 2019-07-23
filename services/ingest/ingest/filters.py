import json


def filter_github(data):
    data_dict = json.loads(data)
    if data_dict.get("repository") and data_dict["repository"].get("private"):
        return None
    return data


def filter_slack(data):
    # Being very careful to only select the data points we need as to not accidentally include some
    # personal information
    data_dict = json.loads(data)
    if "event" not in data_dict:
        return None
    document = {
        "event": {
            "type": "message",
            "channel": data_dict["event"]["channel"]
        },
        "event_time": data_dict["event_time"],
        "team_id": data_dict["team_id"],
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

    document = {
        "event": {
            "type": "reaction_added",
            "item": {
                "channel": channel
            },
            "reaction": data_dict["event"]["reaction"]
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
