"""
Author: Wenhua Yang
Date: 09/18/2016
"""

from flask import Flask, Response, request
import json

from search_api.provider import auth_service, search_service


application = Flask(__name__)


@application.route('/search/<client_id>/<token>', methods=['POST'])
def search(client_id, token):
    # TODO: retry when request failed for each service

    auth_resp = auth_service.verify(client_id, token)
    if 'error_code' in auth_resp:
        return Response(json.dumps(auth_resp), mimetype='application/json')

    query = request.form['query']

    search_resp = search_service.search(query)
    return Response(json.dumps(search_resp), mimetype='application/json')
