import slack_response
from unittest.mock import MagicMock
import json


def test_create_blocks():
    test_events = {
        "a9838a3": {
            "start": "2019-07-05T14:00:00+02:00",
            "summary": "AI summit #1337"
        },
        "8test89": {
            "start": "2019-09-11",
            "summary": "Dataplattform summit #321"
        }
    }
    blocks_correct = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Velg arrangementet du vil bruke knappen på."
                        "\n (Listen er hentet fra google calender, lag event der først om du ikke "
                        "ser den på listen her.)\n Les hvordan du kobler opp her: \n "
                        "https://github.com/knowit/Dataplattform/wiki/Lage-et-arrangement-koblet-opp-mot-vurderingssystemet"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*" + "AI summit #1337* \n 2019-07-05T14:00:00+02:00"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Få kode"

                },
                "value": "a9838a3",
                "action_id": "button",

            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Dataplattform summit #321* \n 2019-09-11"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Få kode"

                },
                "value": "8test89",
                "action_id": "button",

            }
        },
        {
            "type": "divider"
        },

    ]

    # Need to mock slack response in order to skip the dynamoDB part, because at this point we
    # don't want to set up a DynamoDB table just for testing.
    mock_slack_response = slack_response
    mock_slack_response.get_code = MagicMock(return_value=None)

    blocks = slack_response.create_blocks(test_events)

    assert blocks == blocks_correct


def test_create_dialog():
    dialog_correct = {
        "callback_id": "event_test_id",
        "title": "Arrangement",
        "state": "event_test_id",
        "elements": [
            {
                "label": "Hvor mange kom på arrangementet?",
                "name": "number_of_people",
                "type": "text",
                "subtype": "number",
                "placeholder": 100
            },
            {
                "label": "Hvilken faggruppe?",
                "type": "select",
                "name": "guild",
                "options": [
                    {'label': 'Web Chapter', 'value': 'Web Chapter'},
                    {'label': 'Ruby Guild', 'value': 'Ruby Guild'},
                    {'label': 'Security Guild', 'value': 'Security Guild'},
                    {'label': 'Hardware Guild', 'value': 'Hardware Guild'},
                    {'label': 'Kodekino', 'value': 'Kodekino'},
                    {'label': 'Creative crew', 'value': 'Creative crew'},
                    {'label': 'Artificial Chapter', 'value': 'Artificial Chapter'},
                    {'label': 'Rust Guild', 'value': 'Rust Guild'},
                    {'label': 'Rådgivning & ledelse', 'value': 'Rådgivning & ledelse'},
                    {'label': 'User Chapter', 'value': 'User Chapter'},
                    {'label': 'Quality Chapter', 'value': 'Quality Chapter'},
                    {'label': 'JVM Chapter', 'value': 'JVM Chapter'},
                    {'label': 'Architecture Chapter', 'value': 'Architecture Chapter'},
                    {'label': 'Virtual Guild', 'value': 'Virtual Guild'},
                    {'label': 'dotnet Chapter', 'value': 'dotnet Chapter'},
                    {'label': 'Speakers Guild', 'value': 'Speakers Guild'},
                    {'label': 'Engineering Leadership Chapter',
                     'value': 'Engineering Leadership Chapter'},
                    {'label': 'Annen/ ingen', 'value': 'Annen/ ingen'}
                ]
            }

        ]
    }

    dialog = slack_response.create_dialog("event_test_id")
    assert dialog == dialog_correct
