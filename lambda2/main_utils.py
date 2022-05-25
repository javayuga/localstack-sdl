import os
import logging
import json
from zipfile import ZipFile

import boto3

AWS_REGION = 'us-east-1'
AWS_PROFILE = 'localstack'
ENDPOINT_URL = 'http://localhost:4566'
LAMBDA_ZIP = './function.zip'
AWS_CONFIG_FILE = '~/.aws/config'

boto3.setup_default_session(profile_name=AWS_PROFILE)

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


def get_boto3_client(service):
    """
    Initialize Boto3 client.
    """
    try:
        lambda_client = boto3.client(
            service,
            region_name=AWS_REGION,
            endpoint_url=ENDPOINT_URL
        )
    except Exception as e:
        logger.exception('Error while connecting to LocalStack.')
        raise e
    else:
        return lambda_client


def create_lambda_zip(function_name):
    """
    Generate ZIP file for lambda function.
    """
    try:
        with ZipFile(LAMBDA_ZIP, 'w') as zip:
            zip.write('lambda2/{}.py'.format(function_name), arcname='{}.py'.format(function_name))
    except Exception as e:
        logger.exception('Error while creating ZIP file.')
        raise e


def create_lambda(function_name):
    """
    Creates a Lambda function in LocalStack.
    """
    try:
        lambda_client = get_boto3_client('lambda')
        _ = create_lambda_zip(function_name)

        # create zip file for lambda function.
        with open(LAMBDA_ZIP, 'rb') as f:
            zipped_code = f.read()

        lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.8',
            Role='role',
            Handler=function_name + '.handler',
            Code=dict(ZipFile=zipped_code)
        )
    except Exception as e:
        logger.exception('Error while creating function.')
        raise e


def delete_lambda(function_name):
    """
    Deletes the specified lambda function.
    """
    try:
        lambda_client = get_boto3_client('lambda')
        lambda_client.delete_function(
            FunctionName=function_name
        )
        # remove the lambda function zip file
        os.remove(LAMBDA_ZIP)
    except Exception as e:
        logger.exception('Error while deleting lambda function')
        raise e


def invoke_function(function_name):
    """
    Invokes the specified function and returns the result.
    """
    try:
        lambda_client = get_boto3_client('lambda')
        response = lambda_client.invoke(
            FunctionName=function_name)
        return (response['Payload']
                .read()
                .decode('utf-8')
                )
    except Exception as e:
        logger.exception('Error while invoking function')
        raise e


def create_bucket(bucket_name):
    """
    Create a S3 bucket.
    """
    try:
        s3_client = get_boto3_client('s3')
        s3_client.create_bucket(
            Bucket=bucket_name
        )
    except Exception as e:
        logger.exception('Error while creating s3 bucket')
        raise e


def list_s3_bucket_objects(bucket_name):
    """
    List S3 buckets.
    """
    try:
        s3_client = get_boto3_client('s3')
        return s3_client.list_objects_v2(
            Bucket=bucket_name
        )['Contents']
    except Exception as e:
        logger.exception('Error while listing s3 bucket objects')
        raise e


def delete_bucket(bucket_name):
    """
    Delete a S3 bucket.
    """
    try:
        s3_client = get_boto3_client('s3')
        objects = list_s3_bucket_objects(bucket_name)
        # empty the bucket before deleting
        [s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
         for obj in objects]
        s3_client.delete_bucket(
            Bucket=bucket_name
        )
    except Exception as e:
        logger.exception('Error while deleting s3 bucket')
        raise e