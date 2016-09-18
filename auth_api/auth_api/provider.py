"""
Author: Wenhua Yang
Date: 09/18/2016
"""

import requests


class AuthService(object):
    """auth_service provider.
    """

    def __init__(self, server):
        # TODO: service descovery rather than designate server
        self.prefix = server

    def get_token(self, client_id, secret):
        url = '{}/token/{}/{}'.format(self.prefix, client_id, secret)
        response = requests.get(url)
        return response.json()


auth_service = AuthService('http://localhost:7301')
