"""
news_source_reddit.py: Scraping functions for the most read  News Sources of the Reddit Category

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app.aml_utils import getpage, parsepage, get_ns


def __re_any(soup):
    """
    Gets the most read entries of the Ask Reddit/TIL/IAmA  subreddits from the last 24 hours
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Ask Reddit page
    """
    news = []

    anchors = soup.find_all('a')

    i = 0

    for a in anchors:
        if a.has_attr('data-click-id'):
            if a['data-click-id']  == 'body':
                title = a.h3.string.strip()
                # Ignore Requests
                if 'AMA Request' in title:
                    continue
                link = 'https://www.reddit.com' + a['href']
                news.append(dict(title=title, link=link))
                i += 1
                if i == 5:
                    break

    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(re_ask=__re_any, re_science=__re_any, re_life=__re_any, re_world=__re_any,  re_til=__re_any, re_iama=__re_any, re_aww=__re_any, re_bros=__re_any, re_derps=__re_any, re_interestingasfuck=__re_any, re_damnthatsinteresting=__re_any, re_nextfuckinglevel=__re_any)


def get_most_read(key):
    """
    Gets the most read news from a given page

    :param key: the key of the source page (e.g: g1)
    :return: a list with the most read news from the page and the name of news source
    """
    ns = get_ns(key)
    response, content = getpage(ns.url)  # Download the page
    soup = parsepage(content)  # Then we parse it
    strategy = strategies[key]  # Then we execute the selected Strategy based on the source
    return strategy(soup), ns.name
