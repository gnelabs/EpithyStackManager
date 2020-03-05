"""
Specific module to vend service worker files directly through lambda and api gateway.
"""


__author__ = "Nathan Ward"

import os
from views import register_view

#File names are hashed, so get the exact names so they can be registered.
PARTIAL_FILENAMES = {
    'service-worker': '',
    'precache-manifest': '',
    'asset-manifest': ''
}
for filename in os.listdir(os.getcwd()):
    for rf in PARTIAL_FILENAMES:
        if rf in filename:
            PARTIAL_FILENAMES[rf] = filename

def service_worker_files(file: str) -> str:
    """
    Loads and returns the file.
    """
    try:
        with open(os.path.join(os.getcwd(), file), 'r') as javascript_file:
            return {
                'statusCode': 200,
                'body': javascript_file.read(),
                'headers': {'Content-Type': 'application/javascript'}
            }
    except FileNotFoundError:
        return {
           'statusCode': 404,
           'body': json.dumps({'message': 'Not Found.'}),
           'headers': {'Content-Type': 'application/json'}
        }

#Lazy implementation of service-worker file routes. 
@register_view(PARTIAL_FILENAMES['service-worker'])
def a(event, context):
    return service_worker_files(PARTIAL_FILENAMES['service-worker'])

@register_view(PARTIAL_FILENAMES['precache-manifest'])
def b(event, context):
    return service_worker_files(PARTIAL_FILENAMES['precache-manifest'])

@register_view(PARTIAL_FILENAMES['asset-manifest'])
def c(event, context):
    return service_worker_files(PARTIAL_FILENAMES['asset-manifest'])