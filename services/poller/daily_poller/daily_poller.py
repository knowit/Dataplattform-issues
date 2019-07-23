import blog_poller
import ubw_poller


def lambda_handler(event, context):
    res = ubw_poller.poll()
    res2 = blog_poller.poll()
    if res and res2:
        return {
            'statusCode': 200,
            'body': ''
        }

    else:
        return {
            'statusCode': 500,
            'body': ''
        }
