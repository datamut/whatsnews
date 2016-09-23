"""
Author: Wenhua Yang
Date: 09/18/2016
"""

import requests


class AuthService(object):
    """auth_service provider.
    """

    def __init__(self, application):
        # TODO: service discovery rather than designate server
        self.application = application

    def get_token(self, client_id, secret):
        url = '{}/token/{}/{}'.format(
            self.application.config['AUTH_SERVICE_URL'], client_id, secret)
        response = requests.get(url)
        return response.json()
