"""
news_source_international.py: Scraping functions for the most read International News Sources

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from src.utils import util


def __ny(soup):
    """
   Gets the most read news from the NY Times page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the NY Times page
   """
    news = []
    ordered_list = soup.find_all('ol', class_='mostPopularList')[1]  # Second Ordered List of the page
    anchors = ordered_list.find_all('a')

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


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(ny=__ny, wp=__wp, tg=__tg)


def get_most_read(source):
    """
    Gets the most read news from a given page

    :param source: the name of the source page (e.g: g1)
    :return: a list with the most read news from the page
    """
    response, content = util.getpage(util.urls[source])  # First we download the page
    soup = util.parsepage(content)  # Then we parse it
    strategy = strategies[source]  # Then we execute the selected Strategy based on the source
    return strategy(soup), util.friendly_names[source]
