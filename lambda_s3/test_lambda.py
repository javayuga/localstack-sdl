from pip import main
import pytest
import main_utils
import unittest

unittest.TestLoader.sortTestMethodsUsing = None

@pytest.fixture
def policy_bucket():
    bucket_arn = f'arn:aws:s3:::testbucket'
    policy_bucket = main_utils.create_policy(
        'demo-bucket-policy', 'Policy for IAM demonstration.',
        ['s3:ListObjects'], bucket_arn)
    yield policy_bucket
    main_utils.delete_policy('arn:aws:iam::000000000000:policy/demo-bucket-policy')

@pytest.fixture
def policy_lambda():
    logs_arn = f'arn:aws:logs:*:*:*'
    policy_lambda = main_utils.create_policy('demo-lambda-policy', 'Lambda logs',
    ['logs:PutLogEvents','logs:CreateLogGroup','logs:CreateLogStream'], logs_arn)
    yield policy_lambda
    main_utils.delete_policy('arn:aws:iam::000000000000:policy/demo-lambda-policy')

@pytest.fixture
def default_role(policy_lambda):
    role = main_utils.create_iam_role()
    main_utils.attach_iam_policy(role, policy_bucket['Arn'])
    main_utils.attach_iam_policy(role, policy_lambda['Arn'])
    yield role
    main_utils.detach_iam_role(role, policy_lambda['Arn'])
    main_utils.detach_iam_role(role, policy_bucket['Arn'])
    main_utils.delete_iam_role()

@pytest.mark.usefixtures('default_role')
class Test(unittest.TestCase):

    def test_initial_setup(self):
        print('\r\initial setup...')
        assert(default_role) is not None
        print('\r\policies attached...')

        


"""     def test_b_invoke_function_and_response(self):
        print('\r\nInvoke test case...')
        payload = main_utils.invoke_function('lambda')
        bucket_objects = main_utils.list_s3_bucket_objects('testbucket1')
 """
