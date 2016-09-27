"""
Author: Wenhua Yang
Date: 9/27/16

"""

import unittest

from crawler.spiders.theguardian_index_spider import TheGuardianIndexSpider
from crawler.tests import fake_response


class TestTheGuardianIndexSpider(unittest.TestCase):

    def setUp(self):
        self.spider = TheGuardianIndexSpider()

    def test_parse(self):
        url = 'https://www.theguardian.com/au'
        response = fake_response('data/theguardian-1.html', url)
        items = list(self.spider.parse(response))
        self.assertEqual(len(items), 2)
        self.assertEquals(set(map(lambda x: x['url'], items)),
                          {
                          'https://www.theguardian.com/us-news/2016/sep/26/trump-sniffles-presidential-debate-clinton-hofstra',
                          'https://www.theguardian.com/us-news/live/2016/sep/26/hillary-clinton-donald-trump-presidential-debate-live'
                          })

        response = fake_response('data/theguardian-2.html', url)
        items = list((self.spider.parse(response)))
        self.assertEqual(len(items), 103)
        rec_urls = []
        art_urls = []
        for it in items:
            if isinstance(it, dict):
                art_urls.append(it['url'])
            else:
                rec_urls.append(it.url)
        self.assertEqual(len(art_urls), 70)
        self.assertEqual(len(rec_urls), 33)
