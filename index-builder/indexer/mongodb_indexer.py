"""
Author: Wenhua Yang
Date: 09/18/2016
"""

import json
from kafka import KafkaConsumer
import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def run_indexer(mongodb_hosts, kafka_topic, kafka_group, kafka_servers):
    """MongoDB index builder.
    Consume/parse messages from Kafka and save articles to mongodb.
    """

    consumer = KafkaConsumer(kafka_topic, group_id=kafka_group,
                             bootstrap_servers=kafka_servers.split(','))

    with MongoClient(host=mongodb_hosts) as mongo:
        for message in consumer:
            # TODO: how to deal with codec? or ensure utf-8 is correct
            content_str = message.value.decode('utf-8').strip()
            content = json.loads(json.loads(content_str))
            print(content)
            try:
                db = mongo.whatsnews
                db.articles.insert(content)
            except DuplicateKeyError as e:
                # TODO: use log to print exception here
                print(e)


if __name__ == '__main__':
    _mongodb_hosts = os.environ.get('MONGODB_HOSTS')
    assert _mongodb_hosts is not None, \
        'Environment variable MONGODB_HOSTS not found'

    _kafka_topic = os.environ.get('KAFKA_TOPIC')
    assert _kafka_topic is not None, \
        'Environment variable KAFKA_TOPIC not found'

    _kafka_group = os.environ.get('KAFKA_GROUP')
    assert _kafka_group is not None, \
        'Environment variable KAFKA_GROUP not found'

    _kafka_servers = os.environ.get('KAFKA_SERVERS')
    assert _kafka_servers is not None, \
        'Environment variable KAFKA_SERVERS not found'

    run_indexer(mongodb_hosts=_mongodb_hosts, kafka_topic=_kafka_topic,
                kafka_group=_kafka_group, kafka_server=_kafka_servers)
