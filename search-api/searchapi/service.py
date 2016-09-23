"""
Author: Wenhua Yang
Date: 09/18/2016
"""

from flask import Flask, request, render_template, jsonify
import os

from searchapi.provider import AuthService, SearchService


application = Flask(__name__)

auth_service_url = os.environ.get('AUTH_SERVICE_URL', None)
search_service_url = os.environ.get('SEARCH_SERVICE_URL', None)
assert auth_service_url is not None, \
    'Environment variable AUTH_SERVICE_URL not found'
assert search_service_url is not None, \
    'Environment variable SEARCH_SERVICE_URL not found'

application.config.update(dict(
    AUTH_SERVICE_URL=auth_service_url,
    SEARCH_SERVICE_URL=search_service_url
))

auth_service = AuthService(application)
search_service = SearchService(application)


@application.route('/')
def index():
    """A simple web interface of API for better interaction.
    """
    return render_template('index.html')


@application.route('/search/<client_id>/<token>', methods=['POST'])
def search(client_id, token):
    """Search API for external use.
    """

    # TODO: retry when request failed for each service

    auth_resp = auth_service.verify(client_id, token)
    if 'error_code' in auth_resp:
        return jsonify(auth_resp)

    query = request.form['query']
    limit = 10
    if 'limit' in request.form:
        try:
            limit = min(int(request.form['limit']), 100)
        except ValueError:
            pass  # TODO: deal with error here

    result = search_service.search(query, limit)
    return jsonify(result)
