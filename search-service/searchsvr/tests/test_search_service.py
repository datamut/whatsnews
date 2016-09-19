"""
Author: Wenhua Yang
Date: 09/19/2016
"""

import json
import os
import random
import subprocess
import unittest

import pymongo


class TestSearchService(unittest.TestCase):
    def init_db(self):
        """Initialize database, create index.
        """
        self.db_client = pymongo.MongoClient(host=self.db_hosts)
        self.db_client[self.db_name].articles.create_index(
            [
                ("author", pymongo.TEXT),
                ("title", pymongo.TEXT),
                ("summary", pymongo.TEXT),
                ("content", pymongo.TEXT),
            ],
            background=True)
        self.db_client[self.db_name].articles.create_index(
            [("url", pymongo.ASCENDING)],
            unique=True)
        self.db = self.db_client[self.db_name]

    def setUp(self):
        """Setup a new environment. Create db and fill up data.
        """
        db_path = '/tmp/dbpath_test_search_service'
        if not os.path.exists(db_path):
            subprocess.Popen(['mkdir', db_path], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        self.db_name = 'db_whatsnews_{}'.format(int(random.random() * 10000))
        db_port = '27217'
        self.db_hosts = 'mongodb://localhost:{}'.format(db_port)
        subprocess.Popen(['mongod', '--dbpath', db_path, '--port',
                          db_port], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        self.init_db()

        from searchsvr import service
        service.application.config['TESTING'] = True
        service.application.config['MONGO_HOSTS'] = self.db_hosts
        service.application.config['MONGO_DBNAME'] = self.db_name
        self.app_client = service.application.test_client()

    def tearDown(self):
        """Remove db created for test.
        """
        self.db_client.drop_database(self.db_name)

    def search(self, query, limit=20):
        res = self.app_client.post('/search',
                                   data={'query': query, 'limit': limit})
        return json.loads(res.data.decode('utf-8'))

    def test_search(self):
        res = self.search('article')
        self.assertEqual(len(res), 0)

        self.db.articles.insert_one({'title': 'whatsnews search engine',
                                     'author': 'Jack Sun',
                                     'url': 'http://example.com',
                                     'summary': 'A sample article by Jack',
                                     'timestamp': '1237977662000',
                                     'content': 'longer content article'})
        res = self.search('ocean')
        self.assertEqual(len(res), 0)
        for word in ['whatsnews', 'Jack Liu', 'longer article']:
            res = self.search(word)
            self.assertEqual(len(res), 1)
            self.assertEqual(res[0]['url'], 'http://example.com')

        self.db.articles.insert_many([
            {'title': 'Longest fish in the world',
             'author': 'Jack Lin',
             'url': 'http://example.com/path',
             'summary': 'Fish seen in Australia',
             'timestamp': '1237977662001',
             'content': 'Golden Fish Article'},
            {'title': 'run run run',
             'author': 'Runner',
             'url': 'http://example.com/path2',
             'summary': 'Will not appear',
             'timestamp': '1237977662000',
             'content': 'Will not appear'}
        ])

        res = self.search('long')
        self.assertEqual(len(res), 0)
        for word in ['fish jam', 'beautiful world', 'australia', 'Lin']:
            res = self.search(word)
            self.assertEqual(len(res), 1)
            self.assertEqual(res[0]['url'], 'http://example.com/path')

        for word in ['Jack Donald', 'article']:
            res = self.search(word)
            self.assertEqual(len(res), 2)
            # cause result has been sort by score
            self.assertEqual(res[0]['url'], 'http://example.com')
            self.assertEqual(res[1]['url'], 'http://example.com/path')

        res = self.search('article', limit=1)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['url'], 'http://example.com')
