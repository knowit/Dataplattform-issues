class ProcessingData:
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
        out = {
            "negative_emoji": 0,
            "positive_emoji": 0,
            "neutral_emoji": 0
        }
        for reaction_data in data:
            count = reaction_data["count"]

            pos_ratio = reaction_data["positive_ratio"]
            neu_ratio = reaction_data["neutral_ratio"]
            neg_ratio = reaction_data["negative_ratio"]

            if pos_ratio >= neu_ratio and pos_ratio >= neg_ratio:
                emoji_highest = "positive_emoji"
            elif neu_ratio >= pos_ratio and neu_ratio >= neg_ratio:
                emoji_highest = "neutral_emoji"
            elif neg_ratio >= pos_ratio and neg_ratio >= neu_ratio:
                emoji_highest = "negative_emoji"
            else:
                continue
            out[emoji_highest] += count
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

    @staticmethod
    def process_slack_negative_data(data):
        if data["ratio"] is not None:
            ratio = int(data["ratio"])
        else:
            ratio = 0
        return {"slack_negative_ratio": ratio}
