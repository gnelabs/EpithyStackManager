
__author__ = "Nathan Ward"

import os
import zipfile
import logging
import asyncio
import concurrent.futures
from typing import NewType, Any
import boto3
from cfn_lambda.cfnresponse import send, SUCCESS, FAILED

_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.INFO)
Boto3ResourceType = NewType('Boto3ResourceType', boto3.resource)

async def s3_upload_parallel(executor: Any,
                             bucket: Boto3ResourceType,
                             files: list,
                             file_location: str) -> bool:
    """
    Async function to upload files to s3 in parallel.
    """
    loop = asyncio.get_event_loop()
    tasks = []
    for file in files:
        #Hack to make run_in_executor accept params
        bucket_callable = lambda: bucket.upload_file(
            Filename = file,
            Key = file.split(file_location)[1].strip('/')
        )
        tasks.append(
            loop.run_in_executor(
                executor,
                bucket_callable
            )
        )
    
    completed, pending = await asyncio.wait(tasks)
    results = [t.result() for t in completed]
    return results

def lambda_handler(event, context):
    """
    Lambda function that runs on cloudformation create and update.
    Unzips the website static files build and uploads it to s3.
    """
    current_directory = os.getcwd()
    website_version = os.environ['WEBSITE_VERSION']
    
    _LOGGER.info(
        'Unzipping {cwd}/website_{ver}.zip'.format(
            cwd = current_directory,
            ver = website_version
        )
    )
    
    try:
        zipfile_location = '{cwd}/website_{ver}.zip'.format(
            cwd = current_directory,
            ver = website_version
        )
    except KeyError:
        _LOGGER.error('Missing environment variables for lambda to prepare content.')
        send(event, context, FAILED)
        return
    
    #Unzip. Lambda can only write to /tmp.
    with zipfile.ZipFile(zipfile_location, 'r') as zip_ref:
        zip_ref.extractall('/tmp')
    
    assets_folder = '/tmp/build'

    #Walk the files unzipped to get a full path list of what needs
    #to be uploaded to s3.
    file_list = []
    for root, _, filenames in os.walk(assets_folder):
        for filename in filenames:
            file_list.append(os.path.join(root, filename))
    
    bucket_name = os.environ['S3_STATIC_ASSETS_BUCKET']
    _LOGGER.info(
        'Copying static assets version {ver} to S3 bucket {buk}.'.format(
            ver = website_version,
            buk = bucket_name
        )
    )
    s3_resource = boto3.resource('s3')
    destination_bucket = s3_resource.Bucket(bucket_name)
    
    #Set workers to 10, default botocore max conns is 10 and this is good enough.
    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=10,
    )
    loop = asyncio.get_event_loop()
    #Upload files to s3 in parallel. Why? Because there are tons of little static files
    #and it takes forever sequentially.
    s3_upload_results = loop.run_until_complete(
        s3_upload_parallel(
            executor = executor,
            bucket = destination_bucket,
            files = file_list,
            file_location = assets_folder
        )
    )
    
    for upload_result in s3_upload_results:
        if upload_result:
            send(event, context, FAILED)
            return
    
    send(event, context, SUCCESS)
    return