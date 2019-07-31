import json
import urllib.request
import urllib.parse
import os
import pymysql
from datetime import datetime as dt

"""
This lambda gets raw data from the get_docs API and extracts only the valueable information and 
inserts that information into an aurora db. 
"""

# These types will be used if no other types are provided.
DEFAULT_TYPES = [
    "DayRatingType",
    "EventRatingType",
    "EventType",
    "GithubType",
    "SlackType",
    "SlackReactionType",
    "UBWType",
    "KnowitlabsType",
    "YrType",
]

# Assume running hourly by default. Request the last 1h10m of data.
DEFAULT_TIMESTAMP_TO = timestamp = int(dt.now().timestamp())
DEFAULT_TIMESTAMP_FROM = DEFAULT_TIMESTAMP_TO - 70 * 60


def handler(event, context):
    types = DEFAULT_TYPES
    if "types" in event:
        types = event["types"]

    timestamp_from = DEFAULT_TIMESTAMP_FROM
    if "timestamp_from" in event:
        timestamp_from = event["timestamp_from"]

    timestamp_to = DEFAULT_TIMESTAMP_TO
    if "timestamp_to" in event:
        timestamp_to = event["timestamp_to"]

    counter, n_dupes, n_errors = main(types, timestamp_from, timestamp_to)
    return {
        'statusCode': 200,
        'body': f"{counter} records inserted into Aurora. {n_dupes} duplicates skipped. "
        f"{n_errors} errors."
    }


def get_relevant_attrs(docs, type, sql_connection):
    """
    :param docs: Raw documents from get_docs API.
    :param type: which datatype this is.
    :return: only the most relevant attributes which are decided by the Type classes in the
    `data_types` folder.
    """
    # For example: if the type is GithubType we import data_types/GithubType.
    mod = __import__('data_types.' + type, fromlist=[type])
    output = []
    data_type_class = getattr(mod, type)
    data_type_object = data_type_class()

    # To make sure that we are able to insert records into the SQL table we run this now.
    check_table_exists(sql_connection, type, data_type_object)

    n_errors = 0
    for doc in docs:
        try:
            if data_type_object.accept_document(doc):
                column_values = data_type_object.get_column_values(doc)
                if data_type_object.accept_row(column_values):
                    output.append(column_values)
        except:
            n_errors += 1
    return output, n_errors


def check_table_exists(sql_connection, table_name, data_type_object):
    """
    This method checks if a table with name <table_name> already exists or not. If it doesn't
    then it will create a new table.
    :param sql_connection: A MySQL connection.
    :param table_name: Which table should be checked.
    :return:
    """
    # TODO: If the table exists it should check if all the columns are correct.
    cur = sql_connection.cursor()
    test_sql_query = "SELECT 1 FROM " + table_name + " LIMIT 1;"

    exists = True

    try:
        cur.execute(test_sql_query)
    except pymysql.err.ProgrammingError:
        exists = False
        print("No table found, will create new.")

    if not exists:
        sql = data_type_object.get_create_table_sql(table_name)
        cur.execute(sql)


def insert_data_into_db(sql_connection, datas, type):
    """
    :param sql_connection: A MySQL connection.
    :param datas: A list of dictionaries, these dictionaries are containing the key, value that
    make up a SQL record.
    :param type: Which datatype this is. example: GithubType
    :return: The number of records inserted.
    """
    # Just a simple counter to see how many records
    counter = 0
    duplicates = 0
    for data in datas:
        cursor = sql_connection.cursor()

        # This list is just every column name.
        column_list = list(data.keys()).copy()
        # This list is containing every column name surrounded with %()s.
        param_list = ["%(" + column + ")s" for column in column_list]

        params = ", ".join(param_list)
        columns = "`" + "`, `".join(column_list) + "`"
        sql = "INSERT INTO `" + type + "` (" + columns + ") VALUES (" + params + ");"
        try:
            res = cursor.execute(sql, data)
            counter += res
        except pymysql.err.IntegrityError:
            duplicates += 1

    sql_connection.commit()

    return counter, duplicates


def fetch_data_url(url):
    """
    :param url: URL for get_docs API
    :return: list of docs fetched from get_docs API.
    """
    fetch_key = os.getenv("DATAPLATTFORM_FETCH_APIKEY")
    req = urllib.request.Request(url, headers={"x-api-key": fetch_key})
    response = urllib.request.urlopen(req)
    response_dict = json.loads(response.read().decode())
    signed_url = response_dict["all_docs_url"]

    req2 = urllib.request.Request(signed_url)
    response2 = urllib.request.urlopen(req2)
    return json.loads(response2.read().decode())


def format_url(base_url, type, timestamp_from, timestamp_to, just_url=True):
    """
    :return: A formatted url.
    """
    params = {
        "timestamp_from": timestamp_from,
        "timestamp_to": timestamp_to,
        "just_url": just_url
    }
    query = urllib.parse.urlencode(params)
    return base_url + type + "?" + query


def main(types, timestamp_from, timestamp_to):
    base_url = os.getenv("DATAPLATTFORM_FETCH_URL")

    connection = pymysql.connect(
        host=os.getenv("DATAPLATTFORM_AURORA_HOST"),
        port=int(os.getenv("DATAPLATTFORM_AURORA_PORT")),
        user=os.getenv("DATAPLATTFORM_AURORA_USER"),
        password=os.getenv("DATAPLATTFORM_AURORA_PASSWORD"),
        db=os.getenv("DATAPLATTFORM_AURORA_DB_NAME"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    counter = 0
    duplicates = 0
    errors = 0

    for type in types:
        url = format_url(base_url, type, timestamp_from, timestamp_to)
        docs = fetch_data_url(url)
        sql_format, n_errors = get_relevant_attrs(docs, type, connection)
        n_records, n_duplicates = insert_data_into_db(connection, sql_format, type)
        counter += n_records
        duplicates += n_duplicates
        errors += n_errors
    connection.close()
    return counter, duplicates, errors


if __name__ == '__main__':
    number_of_recs_inserted, n_dupes, errors = main(DEFAULT_TYPES, DEFAULT_TIMESTAMP_FROM,
                                                    DEFAULT_TIMESTAMP_TO)
    print(f"Inserted {number_of_recs_inserted} records and skipped {n_dupes} duplicates. "
          f"{errors} errors.")
