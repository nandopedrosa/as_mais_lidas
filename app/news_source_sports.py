"""
news_source_sports.py: Scraping functions for the most read  News Sources of the Sports Category

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app.aml_utils import getpage, parsepage, get_ns


def __e_espn_br(soup):
    """
   Gets the most read news from the ESPN.com.br page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the ESPN  page
   """
    news = []
    ns = get_ns('e_espn_br')

    anchors = soup.find('div', id='most_viewed-all').find_all('a')

    for a in anchors:
        title = a.string
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))

    return news


def __e_fox_br(soup):
    """
    Gets the most read news from the Fox Sports page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Fox Sports page
    """
    news = []
    ns = get_ns('e_fox_br')

    anchors = soup.find('section', class_='home-section most-viewed').find_all('a')

    for a in anchors:
        title = a.h3.string
        link = a['href']
        news.append(dict(title=title, link=link))

    return news


def __e_lance(soup):
    """
    Gets the most read news from the Lance.com.br page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Lance.com.br  page
    """
    news = []
    ns = get_ns('e_lance')

    anchors = soup.find('div', class_='most-read').find_all('a')

    for a in anchors:
        title = a.string
        if title is None:
            continue
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))

    return news


def __e_placar(soup):
    """
    Gets the most read news from the Placar page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Placar page
    """
    news = []
    ns = get_ns('e_placar')

    anchors = soup.find('div', class_='mais-lidas box right').find_all('a')

    for a in anchors:
        title = a.find('h1').string + ': ' + a.find('h2').string
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))

    return news


def __e_gp(soup):
    """
    Gets the most read news from the Grande Premio page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Grande Premio page
    """
    news = []
    ns = get_ns('e_gp')

    anchors = soup.find('div', class_='mhv-mais-lida-posicao').parent.find_all('a')

    for a in anchors:
        title = a.string
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))

    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(e_espn_br=__e_espn_br, e_fox_br=__e_fox_br, e_lance=__e_lance, e_placar=__e_placar, e_gp=__e_gp)


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
