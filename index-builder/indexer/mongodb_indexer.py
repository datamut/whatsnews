"""
Author: Wenhua Yang
Date: 09/18/2016
"""

import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from indexer.message_consumer import ArticleConsumer


def run_indexer(hosts):
    """MongoDB index builder.
    Consume/parse messages from Kafka and save articles to mongodb.
    """

    consumer = ArticleConsumer.new_kafka_consumer()
    with MongoClient(host=hosts) as mongo:
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
    run_indexer('mongodb://localhost:27017')