"""
Author: Wenhua Yang
Date: 09/19/2016
"""

from flask import Flask, request, g, jsonify
import os

from searchsvr.flask_mongo import MongoConnection

mongo_connection = MongoConnection()

application = Flask(__name__)

db_hosts = os.environ.get('MONGODB_HOSTS', None)
db_name = os.environ.get('MONGODB_DBNAME', None)
assert db_hosts is not None, 'Environment variable MONGODB_HOSTS not found'
assert db_name is not None, 'Environment variable MONGODB_DBNAME not found'

application.config.update(dict(
    MONGODB_HOSTS=db_hosts,
    MONGODB_DBNAME=db_name
))


def get_db():
    """Open a new MongoDB connection if there is no connection for
    this context yet.
    """
    if not hasattr(g, 'mongo_db'):
        g.mongo_db = mongo_connection.connect_db(application)
    return g.mongo_db


@application.route('/search', methods=['POST'])
def search():
    db = get_db()
    query = request.form['query']
    limit = int(request.form['limit'])
    cursor = db.articles.find(
        {'$text': {'$search': query}},
        {'_id': 0, 'score': {'$meta': 'textScore'}}
    ).sort([('score', {'$meta': 'textScore'})]).limit(limit)
    result = list(cursor)
    return jsonify(result)


@application.teardown_appcontext
def _teardown(_):
    mongo_connection.close()
