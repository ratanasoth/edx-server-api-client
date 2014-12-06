from distutils.core import setup

setup(
    name='edx-server-api-client',
    version='0.1.0',
    packages=['edx_api_client'],
    url='https://github.com/edx/edx-server-api-client',
    description='Client used to access edX LMS',
    long_description=open('README.rst').read(),
    install_requires=[
        "slumber==0.6.2",
    ],
)
