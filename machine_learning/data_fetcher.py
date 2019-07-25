import pymysql
import os
from datetime import datetime, timedelta


class DataFetcher:
    __connection = None

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
    def fetch_daily_data(date_to=None):
        if date_to is None:
            date_to = datetime.now()
        date_from = date_to - timedelta(days=1)

        timestamp_from = date_from.timestamp()
        timestamp_to = date_to.timestamp()
        x_data = DataFetcher.fetch_x_data(timestamp_from, timestamp_to)
        y_data = DataFetcher.fetch_label(timestamp_from, timestamp_to)
        return x_data, y_data

    @staticmethod
    def fetch_x_data(timestamp_from, timestamp_to):
        results = {}

        def execute_sql_query(data_type, sql_query):
            cursor = DataFetcher.get_connection().cursor()
            cursor.execute(sql_query, (timestamp_from, timestamp_to))
            query_result = cursor.fetchall()
            if len(query_result) > 0:
                results[data_type] = query_result

        slack_sql = "SELECT `slack_timestamp`, `event_type`, `channel_name` FROM `SlackType` WHERE `timestamp`>%s and `timestamp` <%s"
        execute_sql_query("SlackType", slack_sql)

        github_sql = "SELECT `language`, `repository_name`, `commit_timestamp`, `ref` FROM `GithubType` WHERE `timestamp`>%s and `timestamp` <%s"
        execute_sql_query("GithubType", github_sql)

        event_sql = "SELECT `event_name`, `number_of_people`, `group` FROM `EventType` WHERE `timestamp`>%s and `timestamp` <%s"
        execute_sql_query("EventType", event_sql)

        event_rating_sql = "Select `event_name`, sum(button) / count(button) as `ratio` from `EventRatingType` where `timestamp`>%s and `timestamp`<%s GROUP BY `event_name`"
        execute_sql_query("EventRatingType", event_rating_sql)

        return results

    @staticmethod
    def fetch_label(timestamp_from, timestamp_to):
        # TODO: This should do a query similar to the event_rating query.
        return 5 / 6
