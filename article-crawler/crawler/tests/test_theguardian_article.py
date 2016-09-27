"""
Author: Wenhua Yang
Date: 9/24/16

"""

import json
import os
import unittest

from crawler.spiders.theguardian_article import TheGuardianArticleSpider
from crawler.tests import fake_response


class TestTheGuardianArticleSpider(unittest.TestCase):

    def setUp(self):
        self.spider = TheGuardianArticleSpider()

    def test_parse(self):
        json_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 'data/result.json')
        data = json.load(open(json_file, 'r'))
        for file_name, result in data.items():
            url = result['url']
            response = fake_response('data/html/{}'.format(file_name), url)
            item = list((self.spider.parse(response)))[0]
            self.assertEqual(item['title'], result['title'])
            self.assertEqual(item['timestamp'], result['timestamp'])
            self.assertEqual(item['author'], result['author'])
            self.assertEqual(item['summary'], result['summary'])
