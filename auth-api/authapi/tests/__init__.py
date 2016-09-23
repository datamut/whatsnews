"""
Author: Wenhua Yang
Date: 9/23/16

"""

from flask import Flask, jsonify
from flask_loopback.flask_loopback import FlaskLoopback
from urllib.parse import urlparse

from authapi import application

auth_service_url = application.config['AUTH_SERVICE_URL']

auth_app = Flask(__name__)


@auth_app.route("/token/<client_id>/<secret>")
def get_token(client_id, secret):
    if client_id == 'ID123456' and secret == '123456':
        ret = {'token': 'TK123456', 'expires_in': 86400}
    else:
        ret = {'error_code': 3001, 'error_msg': 'invalid client_id or secret'}
    return jsonify(ret)


# TODO: try to reuse this MockServer, it is duplicated with code in search_api
class MockServer(object):
    def __init__(self, app, host, port):
        self.app = app
        self.host = host
        self.port = port
        self.mock_server = FlaskLoopback(app)

    def get_server(self):
        return self.mock_server.on((self.host, self.port))


# TODO: try to reuse this code, it is duplicated with code in search_api
def parse_host_port(url):
    netloc = urlparse(url).netloc
    if ':' not in netloc:
        netloc = '{}:80'.format(netloc)
    _host, _port = netloc.split(':')
    _port = int(_port)
    return _host, _port


# TODO: try to reuse this code, it is duplicated with code in search_api
# this decorator not work for nosetests
def use_mock(mock_server):
    def mock_decorator(func):
        def wrapper(*args, **kwargs):
            with mock_server.get_server():
                func(*args, **kwargs)

        return wrapper

    return mock_decorator


auth_host, auth_port = parse_host_port(auth_service_url)
auth_mock = MockServer(auth_app, auth_host, auth_port)

