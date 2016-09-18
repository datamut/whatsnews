"""
Author: Wenhua Yang
Date: 09/16/2016
"""

import re
from scrapy import Request, Spider

from index_crawler.spiders.spider_base import is_excluded


class TheGuardianIndexSpider(Spider):
    """The Guardian listing page crawler.
    Crosswords and videos were excluded.
    """

    name = 'the_guardian_index'
    start_urls = ['https://www.theguardian.com/au']
    excluded = [
        'https://www.theguardian.com/crosswords/',
        re.compile('.*/video/.*')
    ]

    def parse(self, response):
        """Parser for the guardian website.

        Duplicate urls on current page have been skipped for better performance.

        Simply use <a> tag's data-link-name property to determine whether a
        url is an article page or a listing page. This method is not accurate
        enough. A better solution needs a further research.

        If a certain url is an article url, it will be yield, and if it is a
        listing url, a recursive crawling will be issued.
        """

        urls = {}
        for atag in response.css('div[role="main"] a'):
            utype = atag.xpath('@data-link-name').extract_first()
            href = atag.xpath('@href').extract_first()
            if not href:
                continue

            url = response.urljoin(href)
            if url not in urls and not is_excluded(url, self.excluded):
                # if duplicated, use old one
                urls[url] = utype

        for url, utype in urls.items():
            if utype == 'article':
                yield {'url': url}
            else:
                yield Request(url, callback=self.parse)
