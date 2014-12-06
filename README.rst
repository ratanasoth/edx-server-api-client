edX Server API Client |build-status| |coverage-status|
=========================================================

The edX Server API Client (henceforth, client) allows users to retrieve data from the edX LMS. The current version
supports the retrieval of course info. Future iterations may add support for user, group, and other resources as needed.

This client is a very thin wrapper around the `Slumber`_ library. Please refer to the
Slumber documentation regarding how to make use of the ``Client.courses`` attribute.

..  _Slumber: http://slumber.readthedocs.org/

Testing
-------
    $ make validate


How to Contribute
-----------------

Contributions are very welcome, but for legal reasons, you must submit a signed
`individual contributor's agreement`_ before we can accept your contribution. See our
`CONTRIBUTING`_ file for more information -- it also contains guidelines for how to maintain
high code quality, which will make your contribution more likely to be accepted.

.. _individual contributor's agreement: http://code.edx.org/individual-contributor-agreement.pdf
.. _CONTRIBUTING: https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst

.. |build-status| image:: https://travis-ci.org/edx/edx-server-api-client.svg?branch=master
:target: https://travis-ci.org/edx/edx-server-api-client
.. |coverage-status| image:: https://coveralls.io/repos/edx/edx-server-api-client/badge.png
:target: https://coveralls.io/r/edx/edx-server-api-client
