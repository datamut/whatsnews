# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    """News article item definition.

    title: headline of an article
    author: author of this article
    timestamp: publish timestamp, time in unix format
    url: original url of this article
    summary: summary of this article
    content: article content, readability content(process by redability)
    """

    title = scrapy.Field()
    author = scrapy.Field()
    timestamp = scrapy.Field()
    url = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()
