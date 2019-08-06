from data_types.AbstractType import AbstractType
from data_types.slack_util import get_slack_channel_name
from EmojiSentimentUtil import EmojiSentimentUtil


def match_slack_channel(doc):
    """
    :param doc: The slack event dictionary.
    :return: the channel name of an event.
    """
    channel_id = doc["data"]["event"]["item"]["channel"]
    return get_slack_channel_name(channel_id)


def get_emoji_sentiment(doc, ratio):
    """
    :param doc:
    :param ratio: which ratio you want. should be one of ["positive_ratio" "neutral_ratio",
    "negative_ratio"]
    :return: a number between 0 and 1.
    """
    slack_emoji = doc["data"]["event"]["reaction"]
    if EmojiSentimentUtil.get_sentiment_by_slack_emoji(slack_emoji) is not None:
        return EmojiSentimentUtil.get_sentiment_by_slack_emoji(slack_emoji)[ratio]
    return None


def get_emoji_sentiment_positive(doc):
    return get_emoji_sentiment(doc, "positive_ratio")


def get_emoji_sentiment_neutral(doc):
    return get_emoji_sentiment(doc, "neutral_ratio")


def get_emoji_sentiment_negative(doc):
    return get_emoji_sentiment(doc, "negative_ratio")


class SlackReactionType(AbstractType):
    attributes_keep = {
        ("event_type", str): ["data", "event", "type"],
        ("slack_timestamp", int): ["data", "event_time"],
        ("team_id", str): ["data", "team_id"],
        ("reaction", str): ["data", "event", "reaction"],
        ("channel_name", str, match_slack_channel): [],
        ("positive_ratio", float, get_emoji_sentiment_positive): [],
        ("neutral_ratio", float, get_emoji_sentiment_neutral): [],
        ("negative_ratio", float, get_emoji_sentiment_negative): []
    }
