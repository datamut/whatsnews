# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class ContentWriterPipeline(object):
    # TODO: Merge this with index_crawler's pipelines.
    """Pipeline used to write article content to output file.
    Output format is a json for each row. Each row is a record of an article.
    """

    def __init__(self, out_file):
        """
        Parameters
        ----------
        out_file: string
            output file path, relative path or absolute path is acceptable.
        """
        self.file = open(out_file, 'a+')

    @classmethod
    def from_crawler(cls, crawler):
        """Set output file varible out_file using ARTICLE_OUT_FILE in settings.
        """
        return cls(out_file=crawler.settings.get('ARTICLE_OUT_FILE'))

    def process_item(self, item, spider):
        """Write ArticleItem as json to out_file.
        """
        self.file.write('{}\n'.format(json.dumps(dict(item))))
        return item


class DuplicatesPipeline(object):
    # TODO: Merge this with index_crawler's pipelines.

    def __init__(self):
        self.urls_crawled = set()

    def process_item(self, item, spider):
        url = item['url']
        if url in self.urls_crawled:
            raise DropItem("Url has been crawled: {}".format(url))
        else:
            self.urls_crawled.add(url)
            return item
