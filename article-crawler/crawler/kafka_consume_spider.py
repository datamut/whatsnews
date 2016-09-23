"""
Author: Wenhua Yang
Date: 09/17/2016
"""

import kafka
import scrapy


class KafkaConsumeSpider(scrapy.Spider):
    """This abstract spider integrate Kafka consumer with scrapy.Spider.
    Make it possible to crawl urls from Kafka message.
    """

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """Add a hook here to setup Kafka connect.
        """
        spider = super(KafkaConsumeSpider, cls).from_crawler(crawler, *args,
                                                             **kwargs)
        spider.set_kafka(crawler.settings)
        return spider

    def set_kafka(self, settings):
        """Set Kafka consumer info. Add signals to triger Kafka consume action.

        Raises
        ------
        Raise ValueError when topic, group, or bootstrap_servers is not
        specified.
        """
        topic = settings.get('KAFKA_TOPIC_ID')
        group = settings.get('KAFKA_GROUP_ID')
        servers = settings.get('KAFKA_BOOTSTRAP_SERVERS')
        kafka_servers = servers.split(',')

        self.consumer = kafka.KafkaConsumer(topic, group_id=group,
                                            bootstrap_servers=kafka_servers)
        self.crawler.signals.connect(self.spider_idle,
                                     scrapy.signals.spider_idle)
        self.crawler.signals.connect(self.item_scraped,
                                     scrapy.signals.item_scraped)

    def process_request(self):
        """Process messages from Kafka. Messages from Kafka are urls. It will
        get urls here and crawl these urls.
        """
        message = self.consumer.poll()
        if message:
            for msg_list in message.values():
                for record in msg_list:
                    url = record.value
                    if url:
                        url = url.decode()[
                              1:-1]  # TODO: remove " from kafka-conf?
                        requests = self.make_requests_from_url(url)
                        if requests:
                            self.crawler.engine.crawl(requests, spider=self)

    def spider_idle(self):
        self.process_request()
        raise scrapy.exceptions.DontCloseSpider

    def item_scraped(self, *args, **kwargs):
        self.process_request()
