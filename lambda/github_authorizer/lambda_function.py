import github_authorizer


def lambda_handler(event, context):
    return github_authorizer.handler(event, context)
