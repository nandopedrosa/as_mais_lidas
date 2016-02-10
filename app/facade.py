"""
facade.py: Entry point and validation functions for calling the low level execution functons

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import app.news_source_national as news_source_national
import app.news_source_international as news_source_international


def get_most_read(key):
    """
    Gets the most read news from a given page (national or international)

    :param key: the key of the source page (e.g: g1, localDF, WP, etc.)
    :return: a list with the most read news from the page
    """
    # Check if the News Source is national or internacional
    if key in news_source_national.strategies:
        return news_source_national.get_most_read(key)

    elif key in news_source_international.strategies:
        return news_source_international.get_most_read(key)

    else:
        raise ValueError('No news source found for SOURCE={0}'.format(key))
