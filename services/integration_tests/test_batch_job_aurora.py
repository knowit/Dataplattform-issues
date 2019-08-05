import json

import boto3
import integration_tests_util as util
from datetime import datetime as dt
from integration_tests_util import IntegrationTestUtil

MYSQL_CONFIG = util.read_serverless_output("structured_mysql")
INGEST_CONFIG = util.read_serverless_output("ingest")

ingest_apikey = INGEST_CONFIG["TravisIngestKey"]


def test_dayratingtype_batch():
    body = json.dumps({
        "button": -1
    })
    id, timestamp = ingest("DayRatingType", body)
    invoke_batch_job("DayRatingType", timestamp_from=timestamp)

    row = get_single_row("DayRatingType", id)
    assert row["timestamp"] == timestamp
    assert row["button"] == -1


def test_slacktype_batch():
    type = "SlackType"
    dummy_channel = "C123123"
    dummy_team = "T012341234"
    slack_timestamp = 1564993421
    body = json.dumps({
        "event": {
            "type": "message",
            "channel": dummy_channel
        },
        "event_time": slack_timestamp,
        "team_id": dummy_team
    })

    id, timestamp = ingest(type, body)
    invoke_batch_job(type, timestamp_from=timestamp)
    row = get_single_row(type, id)
    assert row["timestamp"] == timestamp
    assert slack_timestamp != timestamp
    assert row["event_type"] == "message"
    assert row["slack_timestamp"] == slack_timestamp
    assert row["team_id"] == dummy_team
    assert row["channel_name"] is None  # the dummy channel shouldn't match up to anything


def test_githubtype_batch():
    type = "GithubType"
    commit_time = "2019-06-21T13:29:31+02:00"
    stargazers = 1001
    forks_count = 123123
    issue_count = 4321
    body = json.dumps({
        "repository": {
            "full_name": "reponame",
            "stargazers_count": stargazers,
            "language": "SuperAwesomeProgrammingLanguage",
            "forks_count": forks_count,
            "open_issues_count": issue_count
        },
        "sender": {
            "login": "GH_username"
        },
        "head_commit": {
            "id": "headcommitid",
            "timestamp": commit_time
        },
        "ref": "refs/test/test1"
    })
    id, timestamp = ingest(type, body)
    invoke_batch_job(type, timestamp_from=timestamp)
    row = get_single_row(type, id)
    assert row["timestamp"] == timestamp
    assert row["repository_name"] == "reponame"
    assert row["github_username"] == "GH_username"
    assert row["commit_id"] == "headcommitid"
    assert row["commit_timestamp"] == commit_time
    assert row["stargazers_count"] == stargazers
    assert row["language"] == "SuperAwesomeProgrammingLanguage"
    assert row["forks_count"] == forks_count
    assert row["open_issues_count"] == issue_count
    assert row["ref"] == "refs/test/test1"


def ingest(type: str, body: str) -> (str, int):
    ingest_url = INGEST_CONFIG["IngestURL"] + type
    response_code, response_body = util.post_to_api(body, ingest_url, apikey=ingest_apikey)
    assert response_code == 200
    assert "timestamp" in response_body
    assert "id" in response_body
    timestamp = int(response_body["timestamp"])
    id = response_body["id"]
    return id, timestamp


def get_single_row(type, id):
    with IntegrationTestUtil.get_mysql_cursor() as cursor:
        sql = f"SELECT * FROM {type} WHERE id = %s;"
        n_results = cursor.execute(sql, [id])
        assert n_results == 1
        row = cursor.fetchone()
        return row


def invoke_batch_job(type, timestamp_from=None, timestamp_to=None):
    if not timestamp_from:
        timestamp_from = int(dt.now().timestamp()) - 10 * 60  # 10 minutes ago
    if not timestamp_to:
        timestamp_to = int(dt.now().timestamp())

    event = {
        "types": [
            type
        ],
        "timestamp_from": timestamp_from,
        "timestamp_to": timestamp_to
    }
    client = boto3.client('lambda', region_name=MYSQL_CONFIG["region"])
    response = client.invoke(
        FunctionName=MYSQL_CONFIG["batchJobLambda"],
        LogType='None',
        Payload=json.dumps(event).encode()
    )
    assert response["StatusCode"] == 200

    return response


