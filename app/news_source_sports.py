"""
news_source_sports.py: Scraping functions for the most read  News Sources of the Sports Category

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app.aml_utils import getpage, parsepage, get_ns


def __espn(soup):
    """
   Gets the most read news from the ESPN.com.br page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the ESPN  page
   """
    news = []
    ns = get_ns('e_espn')

    anchors = soup.find('div', id='most_viewed-all').find_all('a')

    for a in anchors:
        title = a.string
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))

    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(e_espn=__espn)


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
