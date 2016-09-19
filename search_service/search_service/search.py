"""
Author: Wenhua Yang
Date: 09/19/2016
"""

from flask import Flask, Response, request, g
import json
import pymongo

from search_service.flask_mongo import MongoConnection


mongo_connection = MongoConnection()
app = Flask(__name__)
# MONGODB_HOSTS format: mongodb://[username:password@]host1[:port1][,
#    host2[:port2],...[,hostN[:portN]]][/[database][?options]]
app.config['MONGO_HOSTS'] = 'mongodb://localhost:27017'
app.config['MONGO_DBNAME'] = 'whatsnews'


def get_db():
    """Open a new MongoDB conneciton if there is no connection for
    this context yet.
    """
    if not hasattr(g, 'mongo_db'):
        g.mongo_db = mongo_connection.connect_db(app)
    return g.mongo_db


@app.route('/search', methods=['POST'])
def search():
    db = get_db()
    query = request.form['query']
    cursor = db.articles.find(
            {'$text': {'$search': query}},
            {'_id': 0, 'score': {'$meta': 'textScore'}}
        ).sort([('score', {'$meta': 'textScore'})]).limit(10)
    result = list(cursor)
    return Response(json.dumps(result), mimetype='application/json')


@app.teardown_appcontext
def _teardown(exception):
    mongo_connection.close()
