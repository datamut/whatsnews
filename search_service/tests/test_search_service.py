"""
Author: Wenhua Yang
Date: 09/19/2016
"""

import json
import os
import random
import requests
import subprocess
import pymongo
import unittest


class TestSearchService(unittest.TestCase):
    def init_db(self):
        """Initialize database, create index.
        """
        mongo = pymongo.MongoClient(host=self.dbhosts)
        mongo[self.dbname].articles.create_index(
            [
                ("author", pymongo.TEXT),
                ("title", pymongo.TEXT),
                ("summary", pymongo.TEXT),
                ("content", pymongo.TEXT),
            ],
            background=True)
        mongo[self.dbname].articles.create_index(
            [("url", pymongo.ASCENDING)],
            unique=True)
        return mongo, mongo[self.dbname]

    def setUp(self):
        """Setup a new environment. Create db and fill up data.
        """
        self.dbpath = '/tmp/dbpath_test_search_service'
        if not os.path.exists(self.dbpath):
            p = subprocess.Popen(['mkdir', self.dbpath], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            # TODO: deal with error
            out, err = p.communicate()
        self.dbname = 'db_whatsnews_{}'.format(int(random.random() * 10000))
        self.dbport = '27217'
        self.dbhosts = 'mongodb://localhost:{}'.format(self.dbport)
        subprocess.Popen(['mongod', '--dbpath', self.dbpath, '--port',
                          self.dbport], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        self.mongo, self.db = self.init_db()

        from search_service import search
        search.app.config['TESTING'] = True
        search.app.config['MONGO_HOSTS'] = self.dbhosts
        search.app.config['MONGO_DBNAME'] = self.dbname
        self.client = search.app.test_client()

    def tearDown(self):
        """Remove db created for test.
        """
        self.mongo.drop_database(self.dbname)

    def search(self, query):
        res = self.client.post('/search', data={'query': query})
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
