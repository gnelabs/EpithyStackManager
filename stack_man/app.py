
__author__ = "Nathan Ward"

import json
import os

def lambda_handler(event, context):
    """
    Entry point for the serverless website.
    """
    env_details = {
        'COGNITO_CLIENT_ID': os.environ['COGNITO_CLIENT_ID'],
        'COGNITO_USER_POOL_ID': os.environ['COGNITO_USER_POOL_ID'],
        'COGNITO_USER_UUID': os.environ['COGNITO_USER_UUID'],
        'event_info': event,
        'current_dir': os.listdir(os.getcwd())
    }
    return {
        "statusCode": 200,
        "body": json.dumps(env_details),
    }
