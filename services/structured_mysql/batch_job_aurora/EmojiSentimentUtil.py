import json


class EmojiSentimentUtil:
    __slack_to_unicode_dict = None
    __emoji_sentiment_dict = None

    @staticmethod
    def get_slack_to_unicode_dict():
        """
        :return: A dictionary with short_name (slack emojis) as keys and unicode as values.
        """
        if EmojiSentimentUtil.__slack_to_unicode_dict is None:
            f = open("emoji/emoji_data.json")
            emoji_data = json.loads(f.read())
            f.close()

            slack_to_unicode_dict = {}

            for emoji in emoji_data:
                for short_name in emoji["short_names"]:
                    slack_to_unicode_dict[short_name] = emoji["unified"]

            EmojiSentimentUtil.__slack_to_unicode_dict = slack_to_unicode_dict
        return EmojiSentimentUtil.__slack_to_unicode_dict

    @staticmethod
    def get_emoji_sentiment_dict():
        """
        :return: A dictionary with unicode as input and A dictionary {
                    "positive_ratio": <between 0 and 1>,
                    "neutral_ratio": <between 0 and 1>,
                    "negative_ratio": <between 0 and 1>
                }
        as output.
        """
        if EmojiSentimentUtil.__emoji_sentiment_dict is None:
            f = open("emoji/emoji_sentiment_table.json")
            emoji_data = json.loads(f.read())
            f.close()

            slack_to_unicode_dict = {}

            for emoji_sent in emoji_data:
                negative_emoji_count = emoji_sent["negative"]
                neutral_emoji_count = emoji_sent["neutral"]
                positive_emoji_count = emoji_sent["positive"]
                occurrences = emoji_sent["occurrences"]

                positive_emoji_ratio = positive_emoji_count / occurrences
                neutral_emoji_ratio = neutral_emoji_count / occurrences
                negative_emoji_ratio = negative_emoji_count / occurrences

                unicode = emoji_sent["sequence"]
                slack_to_unicode_dict[unicode] = {
                    "positive_ratio": positive_emoji_ratio,
                    "neutral_ratio": neutral_emoji_ratio,
                    "negative_ratio": negative_emoji_ratio
                }
            EmojiSentimentUtil.__emoji_sentiment_dict = slack_to_unicode_dict
        return EmojiSentimentUtil.__emoji_sentiment_dict

    @staticmethod
    def slack_to_unicode(slack_emoji):
        """
        This method is using the emoji.json taken from https://github.com/iamcal/emoji-data
        :param slack_emoji: Example: thumbs_up if the slack emoji was :thumbsup:.
        :return: the unicode codepoint. example: 1f602
        """
        if slack_emoji in EmojiSentimentUtil.get_slack_to_unicode_dict():
            return EmojiSentimentUtil.get_slack_to_unicode_dict()[slack_emoji]
        return None

    @staticmethod
    def emoji_sentiment(emoji_unicode):
        """
        this method is using the emoji-sentiment-table taken from
        https://github.com/dematerializer/emoji-sentiment/blob/master/res/emoji-sentiment-data.stable.json
        :param emoji_unicode: Unicode codepoint. example: 1f602
        :return: A dictionary {
                    "positive_ratio": <between 0 and 1>,
                    "neutral_ratio": <between 0 and 1>,
                    "negative_ratio": <between 0 and 1>
                }

        """
        if emoji_unicode in EmojiSentimentUtil.get_emoji_sentiment_dict():
            return EmojiSentimentUtil.get_emoji_sentiment_dict()[emoji_unicode]
        return None

    @staticmethod
    def get_sentiment_by_slack_emoji(slack_emoji):
        """
        :param slack_emoji: Example: thumbs_up if the slack emoji was :thumbsup:.
        :return: A dictionary {
                    "positive_ratio": <between 0 and 1>,
                    "neutral_ratio": <between 0 and 1>,
                    "negative_ratio": <between 0 and 1>
                }
        """
        if slack_emoji in EmojiSentimentUtil.get_slack_to_unicode_dict():
            unicode = EmojiSentimentUtil.get_slack_to_unicode_dict()[slack_emoji]
            return EmojiSentimentUtil.emoji_sentiment(unicode)
        return None
