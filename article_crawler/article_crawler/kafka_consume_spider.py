"""
Author: Wenhua Yang
Date: 09/17/2016
"""

import kafka
import scrapy


KAFKA_TOPIC_ID = 'KAFKA_TOPIC_ID'
KAFKA_GROUP_ID = 'KAFKA_GROUP_ID'
KAFKA_BOOTSTRAP_SERVERS = 'KAFKA_BOOTSTRAP_SERVERS'

class KafkaConsumeSpider(scrapy.Spider):

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(KafkaConsumeSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.set_kafka(crawler.settings)
        return spider

    def set_kafka(self, settings):
        topic = settings.get(KAFKA_TOPIC_ID, None)
        if not topic:
            raise ValueError('{} setting is required'.format(KAFKA_TOPIC_ID))

        group = settings.get(KAFKA_GROUP_ID, None)
        if not group:
            raise ValueError('{} setting is required'.format(KAFKA_GROUP_ID))

        servers = settings.get(KAFKA_BOOTSTRAP_SERVERS, None)
        if not servers:
            raise ValueError('{} setting is required'.format(KAFKA_BOOTSTRAP_SERVERS))
        bootstrap_servers = servers.split(',')

        self.consumer = kafka.KafkaConsumer(topic, group_id=group, bootstrap_servers=bootstrap_servers)
        self.crawler.signals.connect(self.spider_idle, scrapy.signals.spider_idle)
        self.crawler.signals.connect(self.item_scraped, scrapy.signals.item_scraped)

    def process_request(self):
        message = self.consumer.poll()
        if message:
            for msg_list in message.values():
                for record in msg_list:
                    url = record.value
                    if url:
                        url = url.decode()[1:-1] # TODO: to remove " from kafka??
                        requests = self.make_requests_from_url(url)
                        if requests:
                            self.crawler.engine.crawl(requests, spider=self)

    def spider_idle(self):
        self.process_request()
        raise scrapy.exceptions.DontCloseSpider

    def item_scraped(self, *args, **kwargs):
        self.process_request()
