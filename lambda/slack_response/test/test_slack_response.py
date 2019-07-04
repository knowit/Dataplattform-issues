import slack_response
from unittest.mock import MagicMock


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
                        "ser den på listen her.) (link til wiki-side på hvordan)"
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
