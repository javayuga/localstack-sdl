import main_utils
import unittest
unittest.TestLoader.sortTestMethodsUsing = None


class Test(unittest.TestCase):
    def test_a_setup_class(self):
        print('\r\nCreate test case...')
        main_utils.create_lambda('lambda')
        main_utils.create_bucket('testbucket1')

    def test_b_invoke_function_and_response(self):
        print('\r\nInvoke test case...')
        payload = main_utils.invoke_function('lambda')
        bucket_objects = main_utils.list_s3_bucket_objects('testbucket1')

    def test_c_teardown_class(self):
        print('\r\nDelete test case...')
        main_utils.delete_lambda('lambda')
        main_utils.delete_bucket('testbucket1')