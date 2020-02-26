
__author__ = "Nathan Ward"

from views import register_view

@register_view('/ping')
def lambda_handler(event, context):
    """
    Unauthenticated route to check availability.
    """
    return {
        'statusCode': 200,
        'body': 'Healthy',
        'headers': {'Content-Type': 'text/html'}
    }