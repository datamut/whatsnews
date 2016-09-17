# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class ContentWriterPipeline(object):

    def __init__(self):
        self.file = open('article_content.txt', 'a+')

    def process_item(self, item, spider):
        self.file.write('{}\n'.format(json.dumps(dict(item))))
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.urls_crawled = set()

    def process_item(self, item, spider):
        url = item['url']
        if url in self.urls_crawled:
            raise DropItem("Url has been crawled: {}".format(url))
        else:
            self.urls_crawled.add(url)
            return item
