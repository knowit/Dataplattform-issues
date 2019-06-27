import batch_job_aurora


def lambda_handler(event, context):
    return batch_job_aurora.handler(event, context)
