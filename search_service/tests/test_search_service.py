"""
Author: Wenhua Yang
Date: 09/19/2016
"""

import json
import os
import random
import subprocess
import pymongo
import unittest


class TestSearchService(unittest.TestCase):
    def init_db(self):
        """Initialize database, create index.
        """
        mongo = pymongo.MongoClient(host=self.db_hosts)
        mongo[self.db_name].articles.create_index(
            [
                ("author", pymongo.TEXT),
                ("title", pymongo.TEXT),
                ("summary", pymongo.TEXT),
                ("content", pymongo.TEXT),
            ],
            background=True)
        mongo[self.db_name].articles.create_index(
            [("url", pymongo.ASCENDING)],
            unique=True)
        return mongo, mongo[self.db_name]

    def setUp(self):
        """Setup a new environment. Create db and fill up data.
        """
        db_path = '/tmp/dbpath_test_search_service'
        if not os.path.exists(db_path):
            p = subprocess.Popen(['mkdir', db_path], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            # TODO: deal with error
            out, err = p.communicate()
        self.db_name = 'db_whatsnews_{}'.format(int(random.random() * 10000))
        db_port = '27217'
        self.db_hosts = 'mongodb://localhost:{}'.format(db_port)
        subprocess.Popen(['mongod', '--dbpath', db_path, '--port',
                          db_port], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        self.mongo, self.db = self.init_db()

        from search_service import search
        search.application.config['TESTING'] = True
        search.application.config['MONGO_HOSTS'] = self.db_hosts
        search.application.config['MONGO_DBNAME'] = self.db_name
        self.client = search.application.test_client()

    def tearDown(self):
        """Remove db created for test.
        """
        self.mongo.drop_database(self.db_name)

    def search(self, query):
        res = self.client.post('/search', data={'query': query, 'limit': 10})
        return json.loads(res.data.decode('utf-8'))

    def test_search(self):
        self.db.articles.insert_one({'title': 'whatsnews search engine',
                                     'author': 'Jack',
                                     'url': 'http://example.com',
                                     'summary': 'A sample article',
                                     'timestamp': '1237977662000',
                                     'content': 'longer content article'})
        res = self.search('ocean')
        self.assertEqual(len(res), 0)
        res = self.search('whatsnews')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['url'], 'http://example.com')
        # some more assertion here

    # TODO: more tests below
    def test_more(self):
        pass
