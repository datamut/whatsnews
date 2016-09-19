"""
Author: Wenhua Yang
Date: 09/19/2016
"""

from flask import Flask, Response, request, g
import json

from searchsvr.flask_mongo import MongoConnection

mongo_connection = MongoConnection()
application = Flask(__name__)
application.config['MONGO_HOSTS'] = 'mongodb://{}@{},{}/whatsnews'.format(
    'ureadonly:u1s2e3r', 'aws-us-east-1-portal.9.dblayer.com:15345',
    'aws-us-east-1-portal.6.dblayer.com:15345'
)
application.config['MONGO_DBNAME'] = 'whatsnews'


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
    return Response(json.dumps(result), mimetype='application/json')


@application.teardown_appcontext
def _teardown(_):
    mongo_connection.close()
