"""
Author: Wenhua Yang
Date: 9/20/16

"""

import json

from searchapi.tests import BaseTestCase, use_mock, auth_mock, search_mock


class TestSearchApi(BaseTestCase):
    def search(self, client_id, token, query, limit=10):
        res = self.app_client.post('/search/{}/{}'.format(client_id, token),
                                   data={'query': query, 'limit': limit})
        return json.loads(res.data.decode('utf-8'))

    @use_mock(auth_mock)
    @use_mock(search_mock)
    def test_search(self):
        res = self.search('ID123456', 'TK123456', 'words', 10)
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0]['url'], 'http://example.com/a')
        self.assertEqual(res[1]['url'], 'http://example.com/b')
        self.assertEqual(res[2]['url'], 'http://example.com/c')

        res = self.search('ID123456', 'TK123456', 'words', 2)
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]['url'], 'http://example.com/a')
        self.assertEqual(res[1]['url'], 'http://example.com/b')

    @use_mock(auth_mock)
    @use_mock(search_mock)
    def test_auth_failed(self):
        res = self.search('ID123456', 'xxx', 'words', 10)
        self.assertTrue(isinstance(res, dict))
        self.assertEqual(res['error_code'], 3002)

        res = self.search('xxx', 'TK123456', 'words', 10)
        self.assertTrue(isinstance(res, dict))
        self.assertEqual(res['error_code'], 3002)

    @use_mock(auth_mock)
    @use_mock(search_mock)
    def test_invalid_input(self):
        res = self.search('ID123456', 'TK123456', '', 10)
        self.assertTrue(isinstance(res, dict))
        self.assertEqual(res['error_code'], 4001)

        res = self.search('ID123456', 'TK123456', 'word', 0)
        self.assertTrue(isinstance(res, dict))
        self.assertEqual(res['error_code'], 4002)

        res = self.search('ID123456', 'TK123456', 'word', -1)
        self.assertTrue(isinstance(res, dict))
        self.assertEqual(res['error_code'], 4002)
