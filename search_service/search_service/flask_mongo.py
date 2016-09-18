

from pymongo import MongoClient


class MongoConnection(object):

    def __init__(self):
        self.connection = None

    def get_db(self, app):
        if self.connection is None:
            hosts = app.config['MONGO_HOSTS']
            self.connection = MongoClient(host=hosts)
            db_name = app.config['MONGO_DBNAME']
            self.db = self.connection[db_name]
        return self.db

    def close(self):
        self.connection.close()
