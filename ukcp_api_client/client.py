"""
client.py
=========

Holds the main client class: UKCPApiClient
"""

import os


from ukcp_api_client.utils import (validate_api_key,
    get_status_url, poll_until_ready)


COMPLETED_STATUS = 'Completed'

KNOWN_STATUS_VALUES = {
    'ProcessStarted': 'Started',
    'ProcessCompleted': 'Completed'
}


class UKCPApiClient(object):
    """
    Main client class: UKCPApiClient.

    Usage:
    >>> cli = UKCPApiClient(api_key='foobaa')
    >>> ...
    """

    def __init__(self, api_key=None):
        """

        :param api_key:
        """
        self._set_api_key(api_key)

    def _set_api_key(self, api_key):
        """

        :param api_key:
        :return:
        """
        api_key = api_key or os.environ.get('API_KEY', None)

        if not api_key:
            raise Exception('Must provide API KEY to client:\n`
                            '\tas API_KEY environment variable\n'
                            '\tor as only argument to UKCPAPIClient(...) call')

        validate_api_key(api_key)
        self._api_key = api_key

    def submit_request(self, request):
        if type(request) is dict:
            request = self._construct_request_url(request)

        request_url = '{}?ApiKey={}'.format(request, self._api_key)

        # Submit request and get Execute Response XML doc
        response = requests.get(request_url)

        # Get status URL
        status_url = get_status_url(response.raw)

        # Poll until a known status is found
        status, response = poll_until_ready(status_url)

        if status != COMPLETED_STATUS:
            return self._respond_to_status(status, response, request_url)








