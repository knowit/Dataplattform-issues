import ingest


def lambda_handler(event, context):
    return ingest.handler(event, context)
