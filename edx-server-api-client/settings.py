"""
Django settings for edx-server-api-client project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from logsettings import get_logger_config


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEFAULT_APPS = (
)

THIRD_PARTY_APPS = (
)

LOCAL_APPS = (
    'api_client',
)

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

WSGI_APPLICATION = 'edx-server-api-client.wsgi.application'

# Api address
# API_SERVER_ADDRESS = 'http://localhost:8000'
API_SERVER_ADDRESS = 'http://openedxapi.apiary-mock.com'
API_MOCK_SERVER_ADDRESS = 'http://openedxapi.apiary-mock.com'

RUN_LOCAL_MOCK_API = False
LOCAL_MOCK_API_FILES = [
    os.path.join(BASE_DIR, 'apiary.apib'),
    os.path.join(BASE_DIR, 'mock_supplementals.apib'),
]

# EdX Api Key
# Set this on OpenEdx server, and within production environment to whichever value is desired
EDX_API_KEY = 'test_api_key'

API_SERVER_PREFIX = '/'.join(['api', 'server'])

# Api locations
COURSEWARE_API = '/'.join([API_SERVER_PREFIX, 'courses'])
GROUP_API = '/'.join([API_SERVER_PREFIX, 'groups'])
ORGANIZATION_API = '/'.join([API_SERVER_PREFIX, 'organizations'])
PROJECT_API = '/'.join([API_SERVER_PREFIX, 'projects'])
AUTH_API = '/'.join([API_SERVER_PREFIX, 'sessions'])
USER_API = '/'.join([API_SERVER_PREFIX, 'users'])
WORKGROUP_API = '/'.join([API_SERVER_PREFIX, 'workgroups'])
