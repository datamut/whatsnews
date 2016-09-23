"""
Author: Wenhua Yang
Date: 9/23/16

Test cases for auth API.
"""

import json
import unittest

from authapi import application
from authapi.tests import auth_mock


class TestAuthAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        application.testing = True
        cls.app_client = application.test_client()

    def test_get_token(self):
        # TODO: use_mock decorator not work for nosetests
        with auth_mock.get_server():
            resp = self.app_client.get('/token/ID123456/123456')
            result = json.loads(resp.get_data(as_text=True))
            self.assertEqual(result.get('token'), 'TK123456')

            resp = self.app_client.get('/token/ID123456/xxx')
            result = json.loads(resp.get_data(as_text=True))
            self.assertEqual(result.get('error_code'), 3001)

            resp = self.app_client.get('/token/xxx/123456')
            result = json.loads(resp.get_data(as_text=True))
            self.assertEqual(result.get('error_code'), 3001)

