"""
Author: Wenhua Yang
Date: 09/18/2016
"""

from flask import Flask, Response, request, render_template
import json

from searchapi.provider import auth_service, search_service


application = Flask(__name__)


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
        return Response(json.dumps(auth_resp), mimetype='application/json')

    query = request.form['query']
    limit = 10
    if 'limit' in request.form:
        try:
            limit = min(int(request.form['limit']), 100)
        except ValueError:
            pass  # TODO: deal with error here

    search_resp = search_service.search(query, limit)
    return Response(json.dumps(search_resp), mimetype='application/json')
