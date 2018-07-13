"""
news_source_technology.py: Scraping functions for the most read Technology News Sources

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app.aml_utils import getpage, parsepage, get_ns
from app.news_source_national import g1


def __tec_g1(soup):
    """
    Gets the most read news from the G1 Technology page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the G1 Technology page
    """
    news = g1(soup)
    return news


def __tec_cw(soup):
    """
    Gets the most read news from the Computer World page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Computer World page
    """
    news = []
    anchors = soup.find('ul', class_='pane').find_all('a')

    for a in anchors:
        if a.img is None:
            title = a.string
            link = a['href']
            news.append(dict(title=title, link=link))
    return news


def __tec_olhar(soup):
    """
    Gets the most read news from the Olhar Digital page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Olhar Digital page
    """
    # DEPRECATED
    news = []
    images = soup.find('div', id='div-gpt-corpo2').next_sibling.next_sibling.find_all('img')

    for img in images:
        title = img['alt']
        link = img.parent['href']
        news.append(dict(title=title, link=link))
    return news


def __tec_conv(soup):
    """
    Gets the most read news from the Convergencia Digital page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Convergencia Digital page
    """
    news = []
    ns = get_ns('tec_conv')

    anchors = soup.find('div', id='slideshow').find_all('a')

    for a in anchors:
        if a.h1:
            title = a.h1.string
            link = 'http://www.convergenciadigital.com.br' + a['href']
            news.append(dict(title=title, link=link))
    return news


def __tec_canal(soup):
    """
    DEPRECATED
    Gets the most read news from the Canaltech page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Canaltech page
    """
    news = []
    ns = get_ns('tec_canal')
    articles = soup.find('section', id='most-readed').find_all('article')

    for article in articles:
        title = article.a.text
        link = article.a['href']
        news.append(dict(title=title, link=link))
    return news


def __tec_uol(soup):
    """
    Gets the most read news from the UOL Tecnologia page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the UOL Tecnologia page
    """
    # DEPRECATED
    news = []
    anchors = soup.find('ol', class_='lst-wrapper').find_all('a')

    for a in anchors:
        title = a.span.string
        link = a['href']
        news.append(dict(title=title, link=link))
    return news


def __tec_giz(soup):
    """
    Gets the most read news from the Gizmodo page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Gizmodo page
    """
    news = []
    li = soup.find('li', class_='selected')
    h3s = li.parent.next_sibling.next_sibling.find_all('h3')

    for h3 in h3s:
        title = h3.a.string
        link = h3.a['href']
        news.append(dict(title=title, link=link))
    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(tec_g1=__tec_g1, tec_cw=__tec_cw, tec_olhar=__tec_olhar, tec_canal=__tec_canal, tec_uol=__tec_uol,
                  tec_giz=__tec_giz, tec_conv=__tec_conv)


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
