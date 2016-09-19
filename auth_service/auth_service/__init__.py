"""
Author: Wenhua Yang
Date: 09/18/2016

This is a fake authorization service. Use static values to ensure the complete
function of this system.
"""


from flask import Flask, Response, request
import json


application = Flask(__name__)

TEST_CLIENT_ID = 'ID123456'
TEST_SECRET = '123456'
TEST_TOKEN = 'TK123456'


@application.route("/token/<client_id>/<secret>")
def get_token(client_id, secret):
    # may have an ip white-list
    ip = request.remote_addr

    if client_id == TEST_CLIENT_ID and secret == TEST_SECRET:
        ret = json.dumps({'token': TEST_TOKEN, 'expires_in': 86400})
    else:
        ret = json.dumps({'error_code': 3001, 'error_msg': 'invalid client_id or secret'})
    return Response(ret, mimetype='application/json')


@application.route("/verify/<client_id>/<token>")
def verify_token(client_id, token):
    if client_id == TEST_CLIENT_ID and token == TEST_TOKEN:
        ret = json.dumps({'valid': True})
    else:
        ret = json.dumps({'error_code': 3002, 'error_msg': 'client_id/token verify failed'})
    return Response(ret, mimetype='application/json')
