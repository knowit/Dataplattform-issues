import get_docs


def lambda_handler(event, context):
    get_docs.handler(event, context)
