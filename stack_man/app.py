
__author__ = "Nathan Ward"

import json

def lambda_handler(event, context):
    """
    Basic lambda function, to be filled in later.
    """
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        }),
    }
