"""
news_source_reddit.py: Scraping functions for the most read  News Sources of the Reddit Category

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app.aml_utils import getpage, parsepage, get_ns
import requests

limit = 5
timeframe = 'today'  # hour, day, week, month, year, all
listing = 'top'  # controversial, best, hot, new, random, rising, top


def __re_any(subreddit):
    """
    Gets the most read entries of the Ask Reddit/TIL/IAmA  subreddits from the last 24 hours
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Ask Reddit page
    """
    posts = []
    base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
    headers = {'User-Agent': 'AsMaisLidas by /u/nandopedrosa'}

    session = requests.Session()

    session.proxies = {
        'http': 'http://159.203.61.169:8080',
    }

    result = session.get(base_url, headers=headers)

    if (result.status_code != 200):
        print("REQUEST RESULT: " + str(result.text))
    json_data = result.json()

    for post in json_data['data']['children']:
        title = post['data']['title']
        link = 'https://www.reddit.com' + post['data']['permalink']
        posts.append(dict(title=title, link=link))
    return posts


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(re_ask=__re_any, re_science=__re_any, re_life=__re_any, re_world=__re_any,  re_til=__re_any, re_iama=__re_any, re_aww=__re_any,
                  re_bros=__re_any, re_derps=__re_any, re_interestingasfuck=__re_any, re_damnthatsinteresting=__re_any, re_nextfuckinglevel=__re_any)


def get_most_read(key):
    """
    Gets the most read news from a given page

    :param key: the key of the source page (e.g: g1)
    :return: a list with the most read news from the page and the name of news source
    """
    ns = get_ns(key)
    strategy = strategies[key]
    return strategy(ns.url), ns.name
