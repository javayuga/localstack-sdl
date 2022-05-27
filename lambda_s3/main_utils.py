import os
import logging
import json
from zipfile import ZipFile
from botocore.exceptions import ClientError

import boto3

AWS_REGION = 'us-east-1'
AWS_PROFILE = 'localstack'
ENDPOINT_URL = 'http://localhost:4566'
LAMBDA_ZIP = './function.zip'
AWS_CONFIG_FILE = '~/.aws/config'

boto3.setup_default_session(profile_name=AWS_PROFILE)

# logger config
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


def get_boto3_client(service):
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


iam = get_boto3_client('iam')

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
    try:
        s3_client = get_boto3_client('s3')
        return s3_client.create_bucket(
            Bucket=bucket_name
        )
    except Exception as e:
        logger.exception('Error while creating s3 bucket')
        raise e


def list_s3_bucket_objects(bucket_name):
    try:
        s3_client = get_boto3_client('s3')
        return s3_client.list_objects_v2(
            Bucket=bucket_name
        )['Contents']
    except Exception as e:
        logger.exception('Error while listing s3 bucket objects')
        raise e


def delete_bucket(bucket_name):
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

def create_policy(name, description, actions, resource_arn):
    """
    Creates a policy that contains a single statement.

    :param name: The name of the policy to create.
    :param description: The description of the policy.
    :param actions: The actions allowed by the policy. These typically take the
                    form of service:action, such as s3:PutObject.
    :param resource_arn: The Amazon Resource Name (ARN) of the resource this policy
                         applies to. This ARN can contain wildcards, such as
                         'arn:aws:s3:::my-bucket/*' to allow actions on all objects
                         in the bucket named 'my-bucket'.
    :return: The newly created policy.
    """
    policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": actions,
                "Resource": resource_arn
            }
        ]
    }
    try:
        policy = iam.create_policy(
            PolicyName=name, Description=description,
            PolicyDocument=json.dumps(policy_doc))['Policy']
        logger.info("Created policy %s.", policy['Arn'])
    except ClientError:
        logger.exception("Couldn't create policy %s.", name)
        raise
    else:
        return policy
# snippet-end:[python.example_code.iam.CreatePolicy]


# snippet-start:[python.example_code.iam.DeletePolicy]
def delete_policy(arn):
    """
    Deletes a policy.

    :param policy_arn: The ARN of the policy to delete.
    """
    try:
        iam.delete_policy(PolicyArn=arn)
        logger.info("Deleted policy %s.", arn)
    except ClientError:
        logger.exception("Couldn't delete policy %s.", arn)
        raise

def list_policies(scope):
    """
    Lists the policies in the current account.

    :param scope: Limits the kinds of policies that are returned. For example,
                  'Local' specifies that only locally managed policies are returned.
    :return: The list of policies.
    """
    try:
        iam = get_boto3_client("iam")
        policies = list()
        paginator = iam.get_paginator('list_policies')
        for response in paginator.paginate(Scope="Local"):
            for policy in response["Policies"]:
                policies.append(policy)
                logger.info(f"Policy Name: {policy['PolicyName']} ARN: {policy['Arn']}")

    except ClientError:
        logger.exception("Couldn't get policies for scope '%s'.", scope)
        raise
    else:
        return policies

def create_iam_role():
    iam = get_boto3_client("iam")

    assume_role_policy_document = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
            }
        ]
    })

    response = iam.create_role(
        RoleName = "lambda-s3-role",
        AssumeRolePolicyDocument = assume_role_policy_document
    )

    return response["Role"]["RoleName"]

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_role
def delete_iam_role():
    iam = get_boto3_client("iam")

    response = iam.delete_role(
        RoleName = "lambda-s3-role"
    )

def attach_iam_policy(role_name, policy_arn):
    iam = get_boto3_client("iam")

    response = iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )

    print(response)

def detach_iam_role(role_name, policy_arn):
    iam = get_boto3_client("iam")

    response = iam.detach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )

    print(response)