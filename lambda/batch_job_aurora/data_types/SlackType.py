from data_types.AbstractType import AbstractType
import os
import json
import urllib.request
import urllib.parse

# This dictionary will be used for caching information about a specific user id and therefore
# saving a lot of time using the slack API.
slack_user_id_to_user_info = {}


def fetch_slack_user_info(user_id):
    """
    This method fetches the user_info using slack's API and saves it in the dict
    `slack_user_id_to_user_info`.
    :param user_id: Which user should be fetched.
    :return:
    """
    # The secret token.
    token = os.getenv("DATAPLATTFORM_AURORA_SLACK_TOKEN")
    base_url = "https://slack.com/api/users.info"
    query = urllib.parse.urlencode({"token": token, "user": user_id})
    url = base_url + "?" + query
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    user = json.loads(response.read().decode())
    slack_user_id_to_user_info[user_id] = user


def fetch_slack_name(doc):
    user_id = doc["data"]["event"]["user"]
    # If the user_id is not cached already then we need to fetch it using Slack's API.
    if user_id not in slack_user_id_to_user_info:
        fetch_slack_user_info(user_id)
    user = slack_user_id_to_user_info[user_id]
    return user["user"]["profile"]["real_name"]


def fetch_slack_username(doc):
    user_id = doc["data"]["event"]["user"]
    if user_id not in slack_user_id_to_user_info:
        fetch_slack_user_info(user_id)
    user = slack_user_id_to_user_info[user_id]
    return user["user"]["name"]


class SlackType(AbstractType):
    attributes_keep = {
        ("event_type", str): ["data", "event", "type"],
        ("user_id", str): ["data", "event", "user"],
        ("channel_id", str): ["data", "event", "channel"],
        ("slack_timestamp", int): ["data", "event_time"],
        ("team_id", str): ["data", "team_id"],
        ("name", str, fetch_slack_name): [],
        ("username", str, fetch_slack_username): [],
    }
