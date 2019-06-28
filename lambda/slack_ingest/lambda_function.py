import slack_ingest


def lambda_handler(event, context):
    return slack_ingest.handler(event, context)
