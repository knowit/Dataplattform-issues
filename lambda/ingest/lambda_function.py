import ingest


def lambda_handler(event, context):
    ingest.handler(event, context)
