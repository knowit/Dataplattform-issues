import json


class ProcessingData:
    __slack_to_unicode_dict = None
    __emoji_sentiment_dict = None

    @staticmethod
    def get_slack_to_unicode_dict():
        if ProcessingData.__slack_to_unicode_dict is None:
            f = open("emoji/emoji_data.json")
            emoji_data = json.loads(f.read())
            f.close()

            slack_to_unicode_dict = {}

            for emoji in emoji_data:
                for short_name in emoji["short_names"]:
                    slack_to_unicode_dict[short_name] = emoji["unified"]

            ProcessingData.__slack_to_unicode_dict = slack_to_unicode_dict
        return ProcessingData.__slack_to_unicode_dict

    @staticmethod
    def get_emoji_sentiment_dict():
        if ProcessingData.__emoji_sentiment_dict is None:
            f = open("emoji/emoji_sentiment_table.json")
            emoji_data = json.loads(f.read())
            f.close()

            slack_to_unicode_dict = {}

            for emoji_sent in emoji_data:
                negative_count = emoji_sent["negative"]
                neutral_count = emoji_sent["neutral"]
                positive_count = emoji_sent["positive"]

                if positive_count >= neutral_count and positive_count >= negative_count:
                    emoji_highest = "positive"
                elif neutral_count >= positive_count and neutral_count >= negative_count:
                    emoji_highest = "neutral"
                elif negative_count >= positive_count and negative_count >= neutral_count:
                    emoji_highest = "negative"
                else:
                    raise Exception("This should never happen...")
                unicode = emoji_sent["sequence"]
                slack_to_unicode_dict[unicode] = emoji_highest
            ProcessingData.__emoji_sentiment_dict = slack_to_unicode_dict
        return ProcessingData.__emoji_sentiment_dict

    @staticmethod
    def process_slack_data(data):
        earlies = 0
        middays = 0
        lates = 0
        for slack_data in data:
            time_of_day = slack_data["time_of_day"]
            if time_of_day == "early":
                earlies += 1
            elif time_of_day == "midday":
                middays += 1
            elif time_of_day == "late":
                lates += 1
        out = {
            "earlies": earlies,
            "middays": middays,
            "lates": lates
        }

        return out

    @staticmethod
    def process_slack_reaction_data(data):
        def slack_to_unicode(slack_emoji):
            """
            This method is using the emoji.json taken from https://github.com/iamcal/emoji-data
            :param slack_emoji: Example: thumbs_up if the slack emoji was :thumbsup:.
            :return: the unicode codepoint. example: 1f602
            """
            if slack_emoji in ProcessingData.get_slack_to_unicode_dict():
                return ProcessingData.get_slack_to_unicode_dict()[slack_emoji]
            return None

        def emoji_sentiment(emoji_unicode):
            """
            this method is using the emoji-sentiment-table taken from
            https://github.com/dematerializer/emoji-sentiment/blob/master/res/emoji-sentiment-data.stable.json
            :param emoji_unicode: Unicode codepoint. example: 1f602
            :return: either "negative", "neutral", "positive", or unknown

            """
            if emoji_unicode in ProcessingData.get_emoji_sentiment_dict():
                return ProcessingData.get_emoji_sentiment_dict()[emoji_unicode]
            return "unknown"

        out = {
            "negative": 0,
            "positive": 0,
            "neutral": 0
        }

        for reaction_data in data:
            unicode = slack_to_unicode(reaction_data["reaction"])
            count = reaction_data["count"]
            if unicode is None:
                # This slack emoji does not have a unicode. It might be a custom slack emoji or the
                # emoji_data.json file might be outdated.
                continue
            sentiment = emoji_sentiment(unicode)
            if sentiment != "unknown":
                out[sentiment] += count
        return out

    @staticmethod
    def process_github_data(data):
        if len(data) == 0:
            count = 0
        else:
            count = data[0]["count"]
        return {"github_count": count}
