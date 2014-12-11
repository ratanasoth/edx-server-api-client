from unittest import TestCase

import httpretty
import requests

from edx_api_client.auth import TokenAuth


class TokenAuthTests(TestCase):
    @httpretty.activate
    def test_headers(self):
        url = 'http://example.com/'
        token = 'token'

        httpretty.register_uri(httpretty.GET, url)
        requests.get(url, auth=TokenAuth(token))
        self.assertEqual(httpretty.last_request().headers['Authorization'], 'Token ' + token)
