"""
Author: Wenhua Yang
Date: 09/19/16

"""

import json
import pymongo

from tests import BaseTestCase


class TestSearchService(BaseTestCase):

    def search(self, query, limit=20):
        res = self.app_client.post('/search',
                                   data={'query': query, 'limit': limit})
        return json.loads(res.data.decode('utf-8'))

    def test_empty(self):
        res = self.search('article')
        self.assertEqual(len(res), 0)

    def test_one(self):
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

        self.db.articles.remove({})

    def test_many(self):
        self.db.articles.insert_many([
            {'title': 'whatsnews search engine',
             'author': 'Jack Sun',
             'url': 'http://example.com',
             'summary': 'A sample article by Jack',
             'timestamp': '1237977662000',
             'content': 'longer content article'},

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

        self.db.articles.remove({})

    def test_insert_error(self):
        self.db.articles.insert_one({'title': 'whatsnews search engine',
                                     'author': 'Jack Sun',
                                     'url': 'http://example.com',
                                     'summary': 'A sample article by Jack',
                                     'timestamp': '1237977662000',
                                     'content': 'longer content article'})
        with self.assertRaises(pymongo.errors.DuplicateKeyError):
            self.db.articles.insert_one({'title': 'whatsnews search engine',
                                         'author': 'Jack Sun',
                                         'url': 'http://example.com',
                                         'summary': 'A sample article by Jack',
                                         'timestamp': '1237977662000',
                                         'content': 'longer content article'})
        self.db.articles.remove({})
