import json


class ProcessingData:
    __slack_to_unicode_dict = None
    __emoji_sentiment_dict = None

    @staticmethod
    def get_slack_to_unicode_dict():
        """
        :return: A dictionary with short_name (slack emojis) as keys and unicode as values.
        """
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
        """
        :return: A dictionary with unicode as input and either "negative_emoji",
        "neutral_emoji" or "positive_emoji"
        as output.
        """
        if ProcessingData.__emoji_sentiment_dict is None:
            f = open("emoji/emoji_sentiment_table.json")
            emoji_data = json.loads(f.read())
            f.close()

            slack_to_unicode_dict = {}

            for emoji_sent in emoji_data:
                negative_emoji_count = emoji_sent["negative"]
                neutral_emoji_count = emoji_sent["neutral"]
                positive_emoji_count = emoji_sent["positive"]

                if positive_emoji_count >= neutral_emoji_count and positive_emoji_count >= \
                        negative_emoji_count:
                    emoji_highest = "positive_emoji"
                elif neutral_emoji_count >= positive_emoji_count and neutral_emoji_count >= \
                        negative_emoji_count:
                    emoji_highest = "neutral_emoji"
                elif negative_emoji_count >= positive_emoji_count and \
                        negative_emoji_count >= neutral_emoji_count:
                    emoji_highest = "negative_emoji"
                else:
                    raise Exception("This should never happen...")
                unicode = emoji_sent["sequence"]
                slack_to_unicode_dict[unicode] = emoji_highest
            ProcessingData.__emoji_sentiment_dict = slack_to_unicode_dict
        return ProcessingData.__emoji_sentiment_dict

    @staticmethod
    def process_slack_data(data):
        """
        :param data: Data to be processed.
        :return: A dictionary containing how many of the slack messages were written early in the
        day, midday and late in the day.
        """
        early_slack_count = 0
        midday_slack_count = 0
        late_slack_count = 0
        for slack_data in data:
            time_of_day = slack_data["time_of_day"]
            if time_of_day == "early":
                early_slack_count += 1
            elif time_of_day == "midday":
                midday_slack_count += 1
            elif time_of_day == "late":
                late_slack_count += 1
        out = {
            "early_slack_count": early_slack_count,
            "midday_slack_count": midday_slack_count,
            "late_slack_count": late_slack_count
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
            :return: either "negative_emoji", "neutral_emoji", "positive_emoji", or unknown

            """
            if emoji_unicode in ProcessingData.get_emoji_sentiment_dict():
                return ProcessingData.get_emoji_sentiment_dict()[emoji_unicode]
            return "unknown"

        out = {
            "negative_emoji": 0,
            "positive_emoji": 0,
            "neutral_emoji": 0
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
        return {"github_count": data["count"]}

    @staticmethod
    def process_event_rating_data(data):
        if data["ratio"] is not None:
            ratio = int(data["ratio"])
        else:
            ratio = 0
        return {"event_rating_ratio": ratio}

    @staticmethod
    def process_weather_data(data):
        if data["temp"] is not None:
            temp = int(data["temp"])
        else:
            temp = 0

        if data["prec"] is not None:
            prec = int(data["prec"])
        else:
            prec = 0
        return {"temperature": temp, "precipitation": prec}
