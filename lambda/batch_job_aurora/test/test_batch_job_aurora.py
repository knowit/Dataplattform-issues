import pytest
import batch_job_aurora
import data_types.GithubType as GithubType
import data_types.AbstractType as AbstractType
import data_types.SlackType as SlackType
import re


def test_format_url():
    base_url = "http://example.org/"
    data_type = "GithubType"
    correct_url = "http://example.org/GithubType?timestamp_from=123&timestamp_to=789"
    timestamp_from = 123
    timestamp_to = 789
    url = batch_job_aurora.format_url(base_url, data_type, timestamp_from, timestamp_to)

    assert url == correct_url


def test_create_abstract_type_fails():
    with pytest.raises(NotImplementedError):
        AbstractType.AbstractType()


def strip_sql_query(sql):
    """
    Just a simple helper method for stripping away the whitespace in sql queries.
    :param sql:
    :return: a stripped sql query.
    """
    sql = sql.replace("\n", "")
    return re.sub('  +', '', sql)


def test_github_sql_create_table():
    github_type = GithubType.GithubType()
    sql = github_type.get_create_table_sql("GithubType")
    sql_correct = """
        CREATE TABLE GithubType (
            `id` VARCHAR(24) NOT NULL,
            `timestamp` BIGINT NOT NULL,
            `repository_name` TEXT,
            `github_username` TEXT,
            `commit_id` TEXT,
            `commit_timestamp` TEXT,
            `stargazers_count` INT,
            `language` TEXT,
            `forks_count` INT,
            `open_issues_count` INT,
            `ref` TEXT,
            PRIMARY KEY (id)
        );"""

    assert strip_sql_query(sql) == strip_sql_query(sql_correct)


def test_get_column_values():
    raw_data = {
        "data": {
            "head_commit": {
                "id": "605417583221e397e13d15b369a9cf6a3ffc9b2e"
            },
            "repository": {
                "name": "Dataplattform",
                "full_name": "Tinusf/Dataplattform"
            },
            "stargazers_count": 0,
            "language": "Python",
            "forks_count": 0
        },
        "pusher": {
            "name": "aslettemark"
        },
        "type": "GithubType",
        "timestamp": 1561372607,
        "id": "AAAAAF0Qp79lNx8dkdk1qQ=="
    }
    github_type = GithubType.GithubType()
    column_values = github_type.get_column_values(raw_data)
    column_values_correct = {
        'id': 'AAAAAF0Qp79lNx8dkdk1qQ==',
        'timestamp': 1561372607,
        'commit_id': '605417583221e397e13d15b369a9cf6a3ffc9b2e',
        'repository_name': 'Tinusf/Dataplattform',
    }

    assert column_values == column_values_correct
    # The raw data does not have a ref therefore it should not be in the column_values variable.
    assert "ref" not in column_values


def test_get_slack_channel_cached():
    # Create a fake channel with a fake user dictionary.
    SlackType.slack_channel_id_to_channel_info["channel123"] = {
        "channel": {"name": "Epic Channel name"},
        "ok": True
    }
    cached_channel = SlackType.get_slack_channel({"data": {"event": {"channel": "channel123"}}})
    assert cached_channel == "Epic Channel name"


def test_deleted_channel():
    SlackType.slack_channel_id_to_channel_info["channel123"] = {
        "ok": False
    }
    cached_channel = SlackType.get_slack_channel({"data": {"event": {"channel": "channel123"}}})
    assert cached_channel is None
