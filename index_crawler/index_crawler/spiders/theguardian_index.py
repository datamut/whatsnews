"""
Author: Wenhua Yang
Date: 09/16/2016
"""

import scrapy


class TheGuardianIndexSpider(scrapy.Spider):

    name = 'the_guardian_index'
    start_urls = ['https://www.theguardian.com/au']

    def parse(self, response):
        list_urls = set()
        article_urls = set() # article url need to remove duplicate
        for atag in response.css('div[role="main"] a'):
            utype = atag.xpath('@data-link-name').extract_first()
            href = atag.xpath('@href').extract_first()
            # TODO: need to deal with href without protocol/domain
            if href:
                url = response.urljoin(href)
                if utype == 'article':
                    article_urls.add(url)
                else:
                    list_urls.add(url)
        for url in article_urls:
            yield {'url': url}
        for url in list_urls:
            yield scrapy.Request(url, callback=self.parse)
