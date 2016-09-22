"""
Author: Wenhua Yang
Date: 09/21/2016
"""

from flask import Flask, Response, request
from flask_loopback.flask_loopback import FlaskLoopback
import json
import unittest
from urllib.parse import urlparse

from searchapi import application

application.testing = True
app_client = application.test_client()

auth_url = application.config['AUTH_SERVICE_URL']
search_url = application.config['SEARCH_SERVICE_URL']


def parse_host_port(url):
    netloc = urlparse(url).netloc
    if ':' not in netloc:
        netloc = '{}:80'.format(netloc)
    _host, _port = netloc.split(':')
    _port = int(_port)
    return _host, _port

auth_host, auth_port = parse_host_port(auth_url)
search_host, search_port = parse_host_port(search_url)

auth_app = Flask(__name__)
search_app = Flask(__name__)


@auth_app.route('/verify/<client_id>/<token>')
def auth_svr(client_id, token):
    if client_id == 'ID123456' and token == 'TK123456':
        ret = json.dumps({'valid': True})
    else:
        ret = json.dumps(
            {'error_code': 3002, 'error_msg': 'client_id/token verify failed'})
    return Response(ret, mimetype='application/json')


@search_app.route('/search', methods=['POST'])
def search_svr():
    if 'query' not in request.form:
        return json.dumps(
            {'error_code': 4001, 'error_msg': 'query cannot be None or empty'})

    query = request.form['query']

    if query is None or len(query) == 0:
        return json.dumps(
            {'error_code': 4001, 'error_msg': 'query cannot be None or empty'})

    limit = int(request.form['limit'])
    if limit <= 0:
        return json.dumps(
            {'error_code': 4002, 'error_msg': 'limit must be grater than 0'})

    data = [
        {
            'url': 'http://example.com/a',
            'timestamp': '1237977662000',
            'content': 'The hardest thing ever',
            'summary': 'Find the way to go to Mars',
            'title': 'The way to Mars',
            'author': 'John Jobs'
        },
        {
            'url': 'http://example.com/b',
            'timestamp': '1237977662001',
            'content': 'Deep in the sea, we can see monsters',
            'summary': 'Find monsters in the ocean',
            'title': 'Fair of ocean',
            'author': 'Stephen Long'
        },
        {
            'url': 'http://example.com/c',
            'timestamp': '1237977662002',
            'content': 'The society we live is out of your imagination.',
            'summary': 'People always lost themselves in crowd',
            'title': 'Understand yourself',
            'author': 'Peter Lee'
        }
    ]
    result = data[:limit]
    return Response(json.dumps(result), mimetype='application/json')


class MockServer(object):
    def __init__(self, app, host, port):
        self.app = app
        self.host = host
        self.port = port
        self.mock_server = FlaskLoopback(app)

    def get_server(self):
        return self.mock_server.on((self.host, self.port))


auth_mock = MockServer(auth_app, auth_host, auth_port)
search_mock = MockServer(search_app, search_host, search_port)


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app_client = app_client


def load_test_suite():
    # load all test cases, use default name tests
    all_tests = unittest.defaultTestLoader.discover('searchapi.tests')
    test_suite = unittest.TestSuite()
    test_suite.addTests(all_tests)
    return test_suite


class BaseTestRunner(unittest.TextTestRunner):
    def run(self, test):
        return super(BaseTestRunner, self).run(test)


def use_mock(mock_server):
    def mock_decorator(func):
        def wrapper(*args, **kwargs):
            with mock_server.get_server():
                func(*args, **kwargs)
        return wrapper
    return mock_decorator
