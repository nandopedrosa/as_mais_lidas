"""
news_source_international.py: Scraping functions for the most read International News Sources

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app.aml_utils import getpage, parsepage, get_ns


def __fox(soup):
    """
   Gets the most read news from the Fox News page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the Fox News page
   """
    news = []
    anchors = soup.find('section', id='trending').find('ol').find_all('a')

    for a in anchors:
        title = a.string
        link = a['href']
        news.append(dict(title=title, link=link))
    return news


def __wp(soup):
    """
   Gets the most read news from the Washington Post page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the Washington Post page
   """
    news = []
    anchors = soup.find('div', id='post-most-rr').find_all('a')

    for a in anchors:
        link = a['href']
        title = a.find('div', class_='headline').string
        news.append(dict(title=title, link=link))
    return news


def __tg(soup):
    """
   Gets the most read news from the The Guardian page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the The Guardian page
   """
    news = []
    anchors = soup.find('div', id='tabs-popular-1').find_all('a')

    for a in anchors:
        link = a['href']
        title = a.text
        news.append(dict(title=title, link=link))
    return news


def __lf(soup):
    """
   Gets the most read news from the Le Figaro page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the Le Figaro page
   """
    news = []
    anchors = soup.find('div', class_='fig-wid-most fig-wid-most-daily').find('ol').find_all('a')

    for a in anchors:
        link = a['href']
        title = a.text
        news.append(dict(title=title, link=link))
    return news


def __tt(soup):
    """
   Gets the most read news from The Telegraph page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the The Telegraph page
   """
    news = []
    ns = get_ns('tt')

    headers = soup.find('div', class_='mostViewedList').find_all('h3', class_='list-of-entities__item-body-headline')

    for h in headers:
        a = h.find('a')
        link = ns.url + a['href']
        title = a.text
        news.append(dict(title=title, link=link))
    return news


def __ep(soup):
    """
   Gets the most read news from El País page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the El País page
   """
    news = []
    anchors = soup.find('div', id='lmv_todo').find_all('a')

    for a in anchors:
        link = a['href']
        # noinspection PyUnusedLocal
        title = 'not-found'

        # Sometimes the item has a Span element (Video icon), sometimes it doesn't
        span = a.find('span')
        if span is None:
            title = a.string
        else:
            title = span.next_sibling.string

        news.append(dict(title=title, link=link))
    return news


def __ny(soup):
    """
   Gets the most read news from NY Times page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the NY Times page
   """
    news = []
    divs = soup.find_all('div', class_='story')

    for d in divs[:10]:
        link = d.h3.a['href']
        title = d.h3.a.string

        news.append(dict(title=title, link=link))
    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(fox=__fox, wp=__wp, tg=__tg, lf=__lf, tt=__tt, ep=__ep, ny=__ny)


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
