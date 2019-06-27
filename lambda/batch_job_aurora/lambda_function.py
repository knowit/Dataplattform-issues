import batch_job_aurora


def lambda_handler(event, context):
    batch_job_aurora.handler(event, context)
