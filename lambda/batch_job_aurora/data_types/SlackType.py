from data_types.AbstractType import AbstractType
import os
import json
import urllib.request
import urllib.parse

# This dictionary will be used for caching information about a specific user id and therefore
# saving a lot of time using the slack API.
# TODO: should we only save the information needed instead of the whole user dictionary?
slack_user_id_to_user_info = {}
slack_channel_id_to_channel_info = {}


def fetch_from_api(base_url, params):
    """
    A helping method for fetching from API.
    :param base_url: The base API url.
    :param params: All the params keys and values needed excluding token.
    :return: the response fetched.
    """
    token = os.getenv("DATAPLATTFORM_AURORA_SLACK_TOKEN")
    params["token"] = token

    query = urllib.parse.urlencode(params)
    url = base_url + "?" + query
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    return json.loads(response.read().decode())


def fetch_slack_channel_info(channel_id):
    """
    This method fetches the channel_info using slack's API and saves it in the dict
    `slack_channel_id_to_channel_info`.
    :param channel_id: Which channel should be fetched.
    :return:
    """
    params = {"channel": channel_id}
    base_url = "https://slack.com/api/channels.info"
    user = fetch_from_api(base_url, params)
    slack_channel_id_to_channel_info[channel_id] = user


def fetch_slack_user_info(user_id):
    """
    This method fetches the user_info using slack's API and saves it in the dict
    `slack_user_id_to_user_info`.
    :param user_id: Which user should be fetched.
    :return:
    """
    params = {"user": user_id}
    base_url = "https://slack.com/api/users.info"
    user = fetch_from_api(base_url, params)
    slack_user_id_to_user_info[user_id] = user


def get_slack_name(doc):
    """
    :param doc:
    :return: The name of the person who made this slack event happen. AKA the sender of a message.
    """
    user_id = doc["data"]["event"]["user"]
    # If the user_id is not cached already then we need to fetch it using Slack's API.
    if user_id not in slack_user_id_to_user_info:
        fetch_slack_user_info(user_id)
    user = slack_user_id_to_user_info[user_id]
    return user["user"]["profile"]["real_name"]


def get_slack_username(doc):
    """
    :param doc:
    :return: The username of a slack sender.
    """
    user_id = doc["data"]["event"]["user"]
    if user_id not in slack_user_id_to_user_info:
        fetch_slack_user_info(user_id)
    user = slack_user_id_to_user_info[user_id]
    return user["user"]["name"]


def get_slack_channel(doc):
    """
    :param doc: The slack event dictionary.
    :return: the channel of an event.
    """
    channel_id = doc["data"]["event"]["channel"]
    if channel_id not in slack_channel_id_to_channel_info:
        fetch_slack_channel_info(channel_id)
    channel = slack_channel_id_to_channel_info[channel_id]
    return channel["channel"]["name"]


class SlackType(AbstractType):
    attributes_keep = {
        ("event_type", str): ["data", "event", "type"],
        ("slack_timestamp", int): ["data", "event_time"],
        ("team_id", str): ["data", "team_id"],
        ("name", str, get_slack_name): [],
        ("username", str, get_slack_username): [],
        ("channel_name", str, get_slack_channel): []
    }
