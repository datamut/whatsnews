"""
Author: Wenhua Yang
Date: 09/17/2016
"""

from readability.readability import Document

from crawler.kafka_consume_spider import KafkaConsumeSpider
from crawler.items import ArticleItem


class TheGuardianArticleSpider(KafkaConsumeSpider):
    """Spider used to crawl and parse articles.
    """

    name = 'the_guardian_article'

    def parse(self, response):
        """Parse url, author, title, timestamp, summary and content.
        """

        url = response.url
        meta = response.css('div.content__meta-container')
        author = meta.xpath('//span[@itemprop="name"]/text()').extract_first()
        if not author:
            author = meta.xpath('//p[@data-component="meta-byline"]/text()')\
                                .extract_first()
        timestamp = meta.xpath(\
            '//time[@itemprop="datePublished"]/@data-timestamp').extract_first()
        # TODO: some tile connot fetch, especially for videos
        title = response.css('h1.content__headline[itemprop="headline"] ::text'\
                             ).extract_first()
        if title:
            title = title.strip()
        summary = response.css('div.content__standfirst').xpath(\
                    '//meta[@itemprop="description"]/@content').extract_first()
        # TODO: get codec from res.headers or res.meta??
        html = response.body.decode('utf-8')

        # TODO: content is not readable enough, some more parameters???
        # TODO: decouple??, move to index_build module?
        content = Document(html).summary()

        item = ArticleItem()
        item['title'] = title
        item['author'] = author
        item['timestamp'] = timestamp
        item['url'] = url
        item['summary'] = summary
        item['content'] = content

        yield item
