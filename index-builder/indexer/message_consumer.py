"""
Author: Wenhua Yang
Date: 09/18/2016
"""

from kafka import KafkaConsumer


class ArticleConsumer(object):
    @classmethod
    def new_kafka_consumer(cls):
        # TODO: use configuration
        return KafkaConsumer('whatsnews_topic_article',
                             group_id='whatsnews_group_article',
                             bootstrap_servers=['localhost:9092'])
