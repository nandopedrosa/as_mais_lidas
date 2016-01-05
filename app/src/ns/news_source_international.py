"""
news_source_international.py: Scraping functions for the most read International News Sources

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from src.utils import util

# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict()


def get_most_read(source):
    """
    Gets the most read news from a given page

    :param source: the name of the source page (e.g: wp)
    :return: a list with the most read news from the page
    """
    pass
