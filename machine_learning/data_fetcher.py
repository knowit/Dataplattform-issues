import pymysql
import os
from datetime import datetime, timedelta
from processing_data import ProcessingData


class DataFetcher:
    __connection = None

    pre_processing_types = {
        "SlackType": ProcessingData.process_slack_data,
        "SlackReactionType": ProcessingData.process_slack_reaction_data,
        "GithubType": ProcessingData.process_github_data,
        "EventRatingType": ProcessingData.process_event_rating_data
    }

    @staticmethod
    def get_connection():
        if DataFetcher.__connection is None:
            DataFetcher()
        return DataFetcher.__connection

    def __init__(self):
        """ Virtually private constructor. """
        if DataFetcher.__connection is not None:
            raise Exception("This class should only be created once.")
        else:
            host = os.getenv("DATAPLATTFORM_AURORA_HOST")
            db_name = os.getenv("DATAPLATTFORM_AURORA_DB_NAME")
            username = os.getenv("DATAPLATTFORM_AURORA_USER")
            password = os.getenv("DATAPLATTFORM_AURORA_PASSWORD")
            port = int(os.getenv("DATAPLATTFORM_AURORA_PORT"))

            connection = pymysql.connect(host=host,
                                         user=username,
                                         password=password,
                                         db=db_name,
                                         port=port,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            DataFetcher.__connection = connection

    @staticmethod
    def fetch_data(date_from, days=1):
        """
        :param date_from: From where do you want to start fetching data.
        :param days: How many days of data do you want to fetch.
        :return: Returns both x_data and labels for all the `days` number of days.
        """
        date_to = date_from + timedelta(days=1)
        x_data_list = []
        label_list = []
        for _ in range(days):
            timestamp_from = date_from.timestamp()
            timestamp_to = date_to.timestamp()
            x_data = DataFetcher.fetch_x_data(timestamp_from, timestamp_to)
            label = DataFetcher.fetch_label(timestamp_from, timestamp_to)

            if label is not None:
                x_data_list.append(x_data)
                label_list.append(label)

            date_to += timedelta(days=1)
            date_from += timedelta(days=1)
        return x_data_list, label_list

    @staticmethod
    def fetch_x_data(timestamp_from, timestamp_to):
        """
        :param timestamp_from: unix timestamp.
        :param timestamp_to: unix timestamp.
        :return: All the features for a specific day.
        """
        results = {
            "weekday": DataFetcher.get_weekday(timestamp_to)
        }

        def execute_sql_query(data_type, sql_query, only_one=False):
            """
            :param data_type: Which data_type is this.
            :param sql_query: The sql query string.
            :param only_one: Only fetch one record.
            :return: Nothing, this just updates the results dictionary with more keys and values.
            """
            cursor = DataFetcher.get_connection().cursor()
            cursor.execute(sql_query, (timestamp_from, timestamp_to))
            if only_one:
                query_result = cursor.fetchone()
            else:
                query_result = cursor.fetchall()
                if len(query_result) > 0 and "timestamp" in query_result[0]:
                    for i in range(len(query_result)):
                        time_of_day = DataFetcher.timestamp_to_time_of_day(
                            query_result[i]["timestamp"])
                        query_result[i]["time_of_day"] = time_of_day
                        del query_result[i]["timestamp"]
            if data_type in DataFetcher.pre_processing_types:
                # If this data needs more processing then we can do that here.
                query_result = DataFetcher.pre_processing_types[data_type](query_result)

            results.update(query_result)

        # TODO: Ideas for more features:
        #  * Which slack channel was talked in.
        #  * Weather
        #  * how many hours used on events this week. (This might be hard because they are quite
        #  delayed).
        #  * train and tram delays.

        # slack_sql = "SELECT COUNT(*) as `count`, `channel_name` FROM `SlackType` WHERE " \
        #             "`timestamp`>%s and `timestamp` <%s and `channel_name` IS NOT NULL GROUP" \
        #             " BY `channel_name` ORDER BY `count` desc"
        slack_sql = "SELECT `timestamp` FROM `SlackType` WHERE `timestamp`>%s AND `timestamp` <%s"
        execute_sql_query("SlackType", slack_sql)

        slack_reactions_sql = "SELECT `reaction`, count(*) AS `count` FROM `SlackReactionType` " \
                              "WHERE `timestamp`>%s AND `timestamp` <%s GROUP BY `reaction`"
        execute_sql_query("SlackReactionType", slack_reactions_sql)

        github_sql = "SELECT COUNT(*) AS `count` FROM `GithubType` WHERE `timestamp`>%s AND " \
                     "`timestamp` <%s"
        execute_sql_query("GithubType", github_sql, only_one=True)

        # This is not grouping by each event. This query calculates the voting ratio of all the
        # events that happened today.
        event_rating_sql = "SELECT (sum(button) / count(button))*1000 AS `ratio` FROM " \
                           "`EventRatingType` WHERE `timestamp`>%s AND `timestamp`<%s"
        execute_sql_query("EventRatingType", event_rating_sql, only_one=True)

        return results

    @staticmethod
    def fetch_label(timestamp_from, timestamp_to):
        """
        :param timestamp_from: unix timestamp.
        :param timestamp_to: unix timestamp.
        :return: Either a number (float) between 0 and 1. or None if there was no ratings between
        the timestamps.
        """
        # In order to get the ratio in the range (0, 1) we add one, and divide by two.
        event_rating_sql = "select (((sum(button) / count(button)) + 1) / 2) as `ratio` from " \
                           "`DayRatingType` where `timestamp`>%s and `timestamp`<%s"
        cursor = DataFetcher.get_connection().cursor()
        cursor.execute(event_rating_sql, (timestamp_from, timestamp_to))
        query_result = cursor.fetchone()
        if query_result["ratio"] is not None:
            return float(query_result["ratio"])
        return None

    @staticmethod
    def timestamp_to_time_of_day(timestamp):
        """
        :param timestamp: unix timestamp.
        :return: Either 'early', 'midday' or 'late'.
        """
        dt_object = datetime.fromtimestamp(timestamp)
        hour = dt_object.hour
        if hour < 10:
            return "early"
        elif hour < 14:
            return "midday"
        else:
            return "late"

    @staticmethod
    def get_weekday(timestamp):
        """
        :param timestamp: unix timestamp.
        :return: a number in the range [0, 6]. 0 is monday etc..
        """
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object.weekday()
