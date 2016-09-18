"""
Author: Wenhua Yang
Date: 09/18/2016
"""

import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from message_consumer import ArticleConsumer


def run_indexer(host, port):
    consumer = ArticleConsumer.new_kafka_consumer()
    with MongoClient(host=host, port=port) as mongo:
        for message in consumer:
            # TODO: how to set codec when send message
            content_str = message.value.decode('utf-8').strip()
            content = json.loads(json.loads(content_str))
            print(content.keys())
            try:
                db = mongo.whatsnews
                db.articles.insert(content)
            except DuplicateKeyError as e:
                # TODO: use log here
                print('****************************************duplicated article found....', e)


if __name__ == '__main__':
    run_indexer('localhost', 27017)
