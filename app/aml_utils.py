"""
util.py: Helper functions and constants common to several News Source operations

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import httplib2
# noinspection PyPackageRequirements
from bs4 import BeautifulSoup
from app.decorators import async_decorator
import json
from app.models import *


def getpage(url):
    """
    Downloads the html page

    :rtype: tuple
    :param url: the page address
    :return: the header response and contents (bytes) of the page
    """
    http = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}

    response, content = http.request(url, headers=headers)
    return response, content


def get_outline(url):
    """
    Gets the Outline link for a Paywall URL

    :param url: the original (paywall) page address
    :return: the new url
    """
    if(url is None):
        return ""

    return "https://12ft.io/" + url


def replace_original_link_with_outline_call(url):
    """
    Replaces the original link with a call to get an outline link

    :param url: the original (paywall) url
    :return: the new url
    """
    return "/outline?original_url=" + url

def parsepage(content):
    """
    Parses a single page and its contents into a BeautifulSoup object

    :param content: bytearray
    :return soup: object
    """
    soup = BeautifulSoup(content, 'lxml')
    return soup


def anchor_has_no_class(tag):
    """
    Helper function. Checks if an anchor tag has class attribute

    :param tag: an HTML tag
    :return: boolean value
    """
    return not tag.has_attr('class') and tag.name == 'a'

def get_ns(key):
    """
    Gets a news_source filtered by key
    :param key: the key of the news source (e.g: g1, uol, etc.)
    :return: the news source object
    """
    ns = NewsSource.query.filter_by(
        key=key).first()  # Fetch news source by key
    return ns
