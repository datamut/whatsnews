"""
Author: Wenhua Yang
Date: 09/18/2016
"""

import requests


class AuthService(object):
    def __init__(self, application):
        self.application = application

    def verify(self, client_id, token):
        url = '{}/verify/{}/{}'.format(
            self.application.config['AUTH_SERVICE_URL'], client_id, token)
        response = requests.get(url)
        return response.json()


class SearchService(object):
    def __init__(self, application):
        self.application = application

    def search(self, query, limit):
        url = '{}/search'.format(self.application.config['SEARCH_SERVICE_URL'])
        data = {'query': query, 'limit': limit}
        response = requests.post(url, data=data)
        return response.json()
