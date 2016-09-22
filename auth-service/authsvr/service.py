"""
Author: Wenhua Yang
Date: 09/18/2016

This is a fake authorization service. Use static values to ensure the complete
function of this system.
"""

from flask import Flask, jsonify

application = Flask(__name__)

TEST_CLIENT_ID = 'ID123456'
TEST_SECRET = '123456'
TEST_TOKEN = 'TK123456'


@application.route("/token/<client_id>/<secret>")
def get_token(client_id, secret):
    # may have an ip white-list
    # ip = request.remote_addr

    if client_id == TEST_CLIENT_ID and secret == TEST_SECRET:
        ret = {'token': TEST_TOKEN, 'expires_in': 86400}
    else:
        ret = {'error_code': 3001, 'error_msg': 'invalid client_id or secret'}
    return jsonify(ret)


@application.route("/verify/<client_id>/<token>")
def verify_token(client_id, token):
    if client_id == TEST_CLIENT_ID and token == TEST_TOKEN:
        ret = {'valid': True}
    else:
        ret = {'error_code': 3002,
               'error_msg': 'client_id/token verify failed'}
    return jsonify(ret)
