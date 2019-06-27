import get_docs


def lambda_handler(event, context):
    return get_docs.handler(event, context)
