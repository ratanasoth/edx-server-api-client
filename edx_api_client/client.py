import slumber

from edx_api_client.auth import TokenAuth


class Client(object):
    """ edX server API client. """

    def __init__(self, base_url, auth_token=None):
        """
        Initialize the client.

        Arguments:
            base_url (str): URL of the API server (e.g. http://courses.edx.org/api/v0)
            auth_token (str): Authentication token
        """
        self._base_url = base_url.rstrip('/')
        self._auth_token = auth_token
        self._api = slumber.API(self._base_url, auth=TokenAuth(self._auth_token))

        self.courses = self._api.courses
