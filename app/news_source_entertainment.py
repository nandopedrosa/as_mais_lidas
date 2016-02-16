"""
news_source_entertainment.py: Scraping functions for the most read  News Sources of the Sports Category

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app.aml_utils import getpage, parsepage, get_ns, anchor_has_no_class


def __en_ego(soup):
    """
    Gets the most read news from the Ego page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Ego page
    """
    news = []
    ns = get_ns('en_ego')

    anchors_famosos = soup.find('div', {"data-evtrk-assunto": "famosos"}).find_all('a', class_='chamada')
    anchors_moda = soup.find('div', {"data-evtrk-assunto": "moda"}).find_all('a', class_='chamada')
    anchors_beleza = soup.find('div', {"data-evtrk-assunto": "beleza"}).find_all('a', class_='chamada')

    anchors = anchors_famosos + anchors_moda + anchors_beleza

    for a in anchors:
        title = a['title']
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))

    return news


def __en_fuxico(soup):
    """
    Gets the most read news from the Fuxico page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Fuxico page
    """
    news = []
    spans = soup.find('div', id='top10_home').find_all('span', class_='ordem')

    for s in spans:
        a = s.parent.next_sibling.next_sibling.a
        title = a.string
        link = 'http://www.ofuxico.com.br' + a['href']
        news.append(dict(title=title, link=link))

    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(en_ego=__en_ego, en_fuxico=__en_fuxico)


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
