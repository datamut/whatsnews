"""
Author: Wenhua Yang
Date: 9/21/16

"""

from searchapi.tests import load_test_suite, BaseTestRunner

if __name__ == '__main__':
    suite = load_test_suite()
    test_runner = BaseTestRunner()
    test_runner.run(suite)
