"""
Author: Wenhua Yang
Date: 9/23/16

Test cases for auth service.
"""

import json
import unittest

from authsvr import application


class TestAuthService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        application.testing = True
        cls.app_client = application.test_client()

    def test_fetch_token(self):
        resp = self.app_client.get('/token/ID123456/123456')
        result = json.loads(resp.get_data(as_text=True))
        self.assertEqual(result.get('token'), 'TK123456')

        resp = self.app_client.get('/token/ID-Invalid/123456')
        result = json.loads(resp.get_data(as_text=True))
        self.assertEqual(result.get('error_code'), 3001)

        resp = self.app_client.get('/token/ID123456/xxx')
        result = json.loads(resp.get_data(as_text=True))
        self.assertEqual(result.get('error_code'), 3001)

    def test_verify_token(self):
        resp = self.app_client.get('/verify/ID123456/TK123456')
        result = json.loads(resp.get_data(as_text=True))
        self.assertEqual(result.get('valid'), True)

        resp = self.app_client.get('/verify/ID123456/xxx')
        result = json.loads(resp.get_data(as_text=True))
        self.assertTrue(result.get('error_code'), 3002)

        resp = self.app_client.get('/verify/xxx/TK123456')
        result = json.loads(resp.get_data(as_text=True))
        self.assertTrue(result.get('error_code'), 3002)
