import json
from unittest import TestCase

import httpretty

from edx_api_client import Client


class ClientTestCase(TestCase):
    def setUp(self):
        self.host = "http://example.com/"
        self.token = "password"
        self.client = Client(self.host, self.token)
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def build_url(self, path=''):
        url = self.host

        if path:
            url = "{0}{1}/".format(url, path)

        return url

    def register_uri(self, method, uri, body='{}'):
        httpretty.register_uri(method, uri, body=body, content_type="application/json")


class ClientTests(ClientTestCase):
    # pylint: disable=protected-access
    def test_init(self):
        self.assertEqual(self.host.rstrip('/'), self.client._base_url)
        self.assertEqual(self.token, self.client._auth_token)
        self.assertIsNotNone(self.client._api)
        self.assertIsNotNone(self.client.courses)


class ClientCoursesTests(ClientTestCase):
    COURSE_ID = 'edX/DemoX/Demo_Course'

    def build_url(self, path=''):
        url = super(ClientCoursesTests, self).build_url('courses')

        if path:
            url = "{0}{1}/".format(url, path)

        return url

    def test_list(self):
        expected = [{'id': self.COURSE_ID}]
        url = self.build_url()
        self.register_uri(httpretty.GET, url, body=json.dumps(expected))
        actual = self.client.courses.get()
        self.assertListEqual(actual, expected)

    def test_detail(self):
        expected = {'id': self.COURSE_ID}
        url = self.build_url(self.COURSE_ID)
        self.register_uri(httpretty.GET, url, body=json.dumps(expected))
        actual = self.client.courses(self.COURSE_ID).get()
        self.assertDictEqual(actual, expected)

    def test_content(self):
        expected = [
            {'id': '1', 'category': 'chapter'},
            {'id': '2', 'category': 'chapter'}
        ]
        url = self.build_url("{0}/{1}".format(self.COURSE_ID, 'content'))
        self.register_uri(httpretty.GET, url, body=json.dumps(expected))
        actual = self.client.courses(self.COURSE_ID).content.get()
        self.assertListEqual(actual, expected)

        # Verify the depth parameter is utilized
        self.client.courses(self.COURSE_ID).content.get(depth=3)
        self.assertEqual(int(httpretty.last_request().querystring['depth'][0]), 3)
