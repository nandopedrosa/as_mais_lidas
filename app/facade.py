"""
facade.py: Entry point and validation functions for calling the low level execution functons

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import app.news_source_national as news_source_national
import app.news_source_international as news_source_international
import app.news_source_sports as news_source_sports
import app.news_source_entertainment as news_source_entertainment
import app.news_source_technology as news_source_technology
import app.news_source_music as news_source_music
import app.news_source_reddit as news_source_reddit


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
    elif key in news_source_sports.strategies:
        return news_source_sports.get_most_read(key)
    elif key in news_source_entertainment.strategies:
        return news_source_entertainment.get_most_read(key)
    elif key in news_source_technology.strategies:
        return news_source_technology.get_most_read(key)
    elif key in news_source_music.strategies:
        return news_source_music.get_most_read(key)
    elif key in news_source_reddit.strategies:
        return news_source_reddit.get_most_read(key)
    else:
        raise ValueError('No news source found for SOURCE={0}'.format(key))
