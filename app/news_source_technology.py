"""
news_source_technology.py: Scraping functions for the most read Technology News Sources

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app.aml_utils import getpage, parsepage, get_ns

def __tec_g1(soup):
    """
    Gets the most read news from the G1 Technology page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the G1 Technology page
    """
    news = []
    anchors = soup.find('ul', class_='highlights').find_all('a')

    for a in anchors:
        title = a.span.string
        link = a['href']
        news.append(dict(title=title, link=link))
    return news

# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(tec_g1=__tec_g1)


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
