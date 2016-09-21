"""
Author: Wenhua Yang
Date: 09/20/2016

Init mongodb and run all test cases.
**Assumption**: For simplicity, we assume that all test cases are in tests
directory and there are no test suite in it.
"""

import os
import unittest
import pymongo


db_hosts = os.environ.get('TEST_MONGO_HOSTS', None)
db_name = os.environ.get('TEST_MONGO_DBNAME', None)
if db_hosts is None:
    assert False, 'variable TEST_MONGO_HOSTS is required'
if db_name is None:
    assert False, 'variable TEST_MONGO_DBNAME is required'


def init_db(_db_hosts, _db_name):
    _db_client = pymongo.MongoClient(host=_db_hosts)
    if _db_name in _db_client.database_names():
        assert False, 'database {} already exists'.format(_db_name)
    _db = _db_client[_db_name]
    _db.articles.create_index([
        ("author", pymongo.TEXT),
        ("title", pymongo.TEXT),
        ("summary", pymongo.TEXT),
        ("content", pymongo.TEXT),
    ], background=True)
    _db.articles.create_index(
        [("url", pymongo.ASCENDING)], unique=True)
    return _db_client, _db


db_client, db = init_db(db_hosts, db_name)


def tear_down():
    db_client.drop_database(db_name)
    db_client.close()


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_client = db_client
        cls.db = db

        from searchsvr import service
        service.application.config['TESTING'] = True
        service.application.config['MONGO_HOSTS'] = db_hosts
        service.application.config['MONGO_DBNAME'] = db_name
        cls.app_client = service.application.test_client()


def load_test_suite():
    # load all test cases, use default name tests
    all_tests = unittest.defaultTestLoader.discover('tests')
    test_suite = unittest.TestSuite()
    test_suite.addTests(all_tests)
    return test_suite


class BaseTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super(BaseTestRunner, self).run(test)
        try:
            tear_down()
        finally:
            return result
