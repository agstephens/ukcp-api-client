"""
utils.py
========

Utility functions and objects for API client.

"""

import time
import re
import requests



def validate_api_key(api_key):
    """
    Checks format of API key looks correct.
    Raises Exception if key is incorrectly formatted.

    :param api_key: API Key [string]
    :return: None
    """
    if len(api_key) != 32:
        raise Exception('API Key must be 32 characters long.')

    if re.search('[^A-Za-z0-9\-_]', api_key) or key[0] in "-_" or key[-1] in "-_":
        raise Exception('API Key must only contain letters, numbers and "-", "_".'
                        ' Must begin and end with a letter or number.')

def get_status_url(xml):
    """

    :param xml:
    :return:
    """
    return status_url


def get_status( xml):
    """

    :param xml:
    :return:
    """
    return status


def poll_until_ready(status_url):
    """

    :param status_url:
    :return:
    """
    status = None

    while status not in KNOWN_STATUS_VALUES:
        time.sleep(5)
        response = requests.get(status_url)
        status = get_status(response.raw)

    return status, response