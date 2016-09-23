"""
Author: Wenhua Yang
Date: 9/21/16

Test of this project needs mongodb connection and will have crud on database.
In order to keep it simple, we create a single thread, one-time database
connection test suite here.

How to run test?
If you work on linux shell, please use following command:
```shell
MONGODB_HOSTS=mongodb://localhost:27017 MONGODB_DBNAME=db1 python run_test.py
```
*Note that MONGODB_HOSTS and MONGODB_DBNAME can be set as environment
variable.*
Other platform or travis can set variables like wise.
"""

from searchsvr.tests import load_test_suite, BaseTestRunner

if __name__ == '__main__':
    suite = load_test_suite()
    test_runner = BaseTestRunner()
    test_runner.run(suite)
