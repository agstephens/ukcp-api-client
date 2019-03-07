"""
client.py
=========

Holds the main client class: UKCPAPIClient
"""

import requests
import os
import time

COMPLETED_STATUS = 'Completed'
KNOWN_STATUS_VALUES = {
    'ProcessStarted': 'Started',
    'ProcessCompleted': 'Completed'
}


class UKCPAPIClient(object):

    def __init__(self, api_key=None):
        self._set_api_key(api_key)

    def _set_api_key(self, api_key):
        api_key = api_key or os.environ.get('API_KEY', None)

        if not api_key:
            raise Exception('Must provide API KEY to client:\n`
                            '\tas API_KEY environment variable\n'
                            '\tor as only argument to UKCPAPIClient(...) call')

            # - check length/content
        self._api_key = api_key

    def

        def submit_request(self, request):
            if type(request) is dict:
                request = self._construct_request_url(request)

            request_url = '{}?ApiKey={}'.format(request, self._api_key)

            # Submit request and get Execute Response XML doc
            response = requests.get(request_url)

            # Get status URL
            status_url = self._get_status_url(response.raw)

            # Poll until a known status is found
            status, response = self._poll_until_ready(status_url)

            if status != COMPLETED_STATUS:
                return self._respond_to_status(status, response, request_url)

    def _poll_until_ready(self, status_url):

        status = None
        while status not in KNOWN_STATUS_VALUES:
            time.sleep(5)
            response = requests.get(request_url)
            status = self._get_status(response.raw)

    return status, response


def _get_status_url(self, xml):
    return status_url


def _get_status(self, xml):
    return status




