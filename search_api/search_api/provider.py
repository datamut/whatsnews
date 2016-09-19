"""
Author: Wenhua Yang
Date: 09/18/2016
"""

import requests


class AuthService(object):

    def __init__(self, server):
        self.prefix = server

    def verify(self, client_id, token):
        url = '{}/verify/{}/{}'.format(self.prefix, client_id, token)
        response = requests.get(url)
        return response.json()


class SearchService(object):

    def __init__(self, server):
        self.prefix = server

    def search(self, query):
        url = '{}/search'.format(self.prefix)
        data = {'query': query}
        response = requests.post(url, data=data)
        return response.json()


auth_service = AuthService('http://authsvr.kc7ctmpd2z.us-west-2.elasticbeanstalk.com')
search_service = SearchService('http://searchsvr.kc7ctmpd2z.us-west-2.elasticbeanstalk.com')
