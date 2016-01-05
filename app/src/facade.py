"""
facade.py: Entry point and validation functions for calling the low level execution functons

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

from src.ns import news_source_national
from src.ns import news_source_international


def get_most_read(source):
    """
    Gets the most read news from a given page (national or international)

    :param source: the name of the source page (e.g: g1, WP, etc.)
    :return: a list with the most read news from the page
    """
    # Check if the News Source is national or internacional
    if source in news_source_national.strategies:
        return news_source_national.get_most_read(source)
    elif source in news_source_international.strategies:
        return news_source_international.get_most_read(source)
    else:
        raise ValueError('No news source found for SOURCE={0}'.format(source))
