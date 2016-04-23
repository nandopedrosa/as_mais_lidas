"""
news_source_music.py: Scraping functions for the most read  News Sources of the Music Category

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app.aml_utils import getpage, parsepage, get_ns


def __m_rs(soup):
    """
   Gets the most read news from the Rolling Stone page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the Rolling Stone page
   """
    news = []
    ns = get_ns('m_rs')

    ul = soup.find('div', class_='most-viewed').find('ul')
    anchors = ul.find_all('a')

    for a in anchors:
        title = a.string
        link = 'http://www.rollingstone.com' + a['href']
        news.append(dict(title=title, link=link))

    return news


def __m_whiplash(soup):
    """
   Gets the most read news from the Whiplash page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the Whiplash page
   """
    news = []
    ns = get_ns('m_whiplash')

    anchors = soup.find('table', class_='tabela').find_all('a')
    i = 0;

    for a in anchors:
        title = a.string
        link = a['href']
        news.append(dict(title=title, link=link))
        i += 1
        if i == 10:
            break

    return news


def __m_revolver(soup):
    """
   Gets the most read news from the Revolver page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the Revolver page
   """
    news = []
    ns = get_ns('m_revolver')

    anchors = soup.find('li', id='wpp-3').find_all('a', class_='wpp-post-title')

    for a in anchors:
        title = a.string
        link = a['href']
        news.append(dict(title=title, link=link))

    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(m_rs=__m_rs, m_whiplash=__m_whiplash, m_revolver=__m_revolver)


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
