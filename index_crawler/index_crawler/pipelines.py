# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class IndexWriterPipeline(object):
    """Pipeline used to write article urls into a file, which is defined in
    settings as INDEX_OUT_FILE. Write mode is append.
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
        """Set output file varible out_file using INDEX_OUT_FILE in settings.
        """
        return cls(out_file=crawler.settings.get('INDEX_OUT_FILE'))

    def process_item(self, item, spider):
        """Only write url to output file.
        """
        self.file.write('{}\n'.format(item['url']))
        return item


class DuplicatesPipeline(object):
    """A simple pipeline used to skip duplicated urls. It is very simple that
    only store visited urls in local memory of current process. A better approch
    of skipping visited urls will need a external memory or tools.
    """

    def __init__(self):
        """Initialize a local set to store visited urls.
        """
        self.urls_crawled = set()

    def process_item(self, item, spider):
        """If a certain url is in this local set, skip it, otherwise, visit it
        and add it to this local set.
        """
        url = item['url']
        if url in self.urls_crawled:
            raise DropItem("Url has been crawled: {}".format(url))
        else:
            self.urls_crawled.add(url)
            return item
