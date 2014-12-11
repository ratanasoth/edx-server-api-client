from requests.auth import AuthBase


class TokenAuth(AuthBase):
    """ Attaches Token Authentication to the given Request object. """

    def __init__(self, token):
        """ Instantiate the auth class. """
        self.token = token

    def __call__(self, r):
        """ Update the request headers. """
        r.headers['Authorization'] = 'Token {0}'.format(self.token)
        return r
