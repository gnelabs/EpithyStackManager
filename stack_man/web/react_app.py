
__author__ = "Nathan Ward"

def lambda_handler(event, context):
    """
    Root website view. I.e. '/' and client-side routes.
    """
    return {
        'statusCode': 200,
        'body': 'Hello World.',
        'headers': {'Content-Type': 'text/html'}
    }