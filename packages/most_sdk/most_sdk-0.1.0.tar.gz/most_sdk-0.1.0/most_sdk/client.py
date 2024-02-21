import os

import requests

from .exceptions import APIError, AuthenticationError, ClientError
from .routes import Enrichment


class Client(object):
    """
    A client for accessing MOST API.
    """

    def __init__(
        self,
        client_key: str = None,
        env: str = None,
    ):
        """Initializes the most_sdk Client
        :param str client_key: Token to generate Basic Authentication bearer
        :param str env: The environment in which API calls will be made
        :rtype: most_sdk.client.Client
        """

        self.env = env or os.environ.get('MOST_SDK_ENV', 'staging')
        self.client_key = client_key or os.environ.get('MOST_SDK_CLIENT_KEY')

        base_url = {
            'prod': 'https://production-mostqiapi.com',
            'staging': 'https://mostqiapi.com',
        }

        try:
            self.base_url = base_url[self.env.strip().lower()]
        except KeyError as e:
            raise ClientError("Use 'prod' or 'staging' as env") from e

        if not self.client_key:
            raise AuthenticationError('Undefined token')

        self.authenticate()

        self._enrichment = None

    @property
    def enrichment(self):
        if not self._enrichment:
            self._enrichment = Enrichment(self)
        return self._enrichment

    def authenticate(self):
        data = {'token': self.client_key}

        response = requests.post(
            url=f'{self.base_url}/user/authenticate',
            json=data,
        )

        response.raise_for_status()

        self.token = response.json()['token']
        self.set_session()

    def set_session(self):
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.token}'})

    def post(self, path, original_data):
        response = self.session.post(url=f'{self.base_url}/{path}', json=original_data)
        data = response.json()

        if response.status_code == 401:
            self.authenticate()
            return self.post(path, original_data)

        if response.status_code == 400:
            raise APIError(data.get('status'))

        response.raise_for_status()

        return data.get('result')
