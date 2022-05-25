import logging

import boto3

AWS_REGION = 'us-east-1'
LOCALSTACK_INTERNAL_ENDPOINT_URL = 'http://host.docker.internal:4566'

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


def get_boto3_client(service):
    """
    Initialize Boto3 client.
    """
    try:
        boto3_client = boto3.client(
            service,
            region_name=AWS_REGION,
            endpoint_url=LOCALSTACK_INTERNAL_ENDPOINT_URL
        )
    except Exception as e:
        logger.exception('Error while connecting to LocalStack.')
        raise e
    else:
        return boto3_client

def handler(event, context):
    s3_client = get_boto3_client('s3')
    logging.info('Uploading an object to the localstack s3 bucket...')
    object_key = 'hands-on-cloud'
    s3_client.put_object(
        Bucket='testbucket1',
        Key=object_key,
        Body='localstack-boto3-python'
    )
    return {
        "message": "Object uploaded to S3."
    }