
__author__ = "Nathan Ward"

import json
import views

def lambda_handler(event, context):
    """
    Entry point for the serverless website.
    Routes the request to the appropriate view.
    """
    try:
        #Normal routes.
        if event['path'] in views.REGISTER:
            return views.REGISTER[event['path']](event, context)
        #Static files in s3.
        elif '/assets/' in event['path'] or '/static/' in event['path']:
            return views.lambda_handler(event, context)
        elif '/service-worker' in event['path'] or '/precache-manifest' in event['path'] or '/asset-manifest' in event['path']:
            return views.lambda_handler(event, context)
        else:
            return {
               'statusCode': 404,
               'body': json.dumps({'message': 'Not Found.'}),
               'headers': {'Content-Type': 'application/json'}
            }
    except KeyError:
        return {
               'statusCode': 500,
               'body': json.dumps({'message': 'Unable to process request.'}),
               'headers': {'Content-Type': 'application/json'}
            }