"""
news_source_entertainment.py: Scraping functions for the most read  News Sources of the Entertainment Category

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app.aml_utils import getpage, parsepage, get_ns, anchor_has_no_class


def __en_om_filmes(soup):
    """
    Gets the most read news from the Omelete Filmes page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Omelete Filmes page
    """
    return __get_omelete_news(soup)


def __en_om_series(soup):
    """
    Gets the most read news from the Omelete Séries page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Omelete Séries page
    """
    return __get_omelete_news(soup)


def __en_om_hqs(soup):
    """
    Gets the most read news from the Omelete Filmes page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Omelete HQs page
    """
    return __get_omelete_news(soup)


def __get_omelete_news(soup):
    """
    Helper function to get Omelete News
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from a given Omelete Page
    """
    news = []

    list_items = soup.find('div', class_='pyquery-ajax-omeletop').find_all('li')

    for item in list_items:
        link = 'http://www.omelete.com.br' + item['data-url']
        title = item['data-name']
        news.append(dict(title=title, link=link))

    return news


def __en_ego(soup):
    """
    Gets the most read news from the Ego page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Ego page
    """
    # DEPRECATED
    news = []
    ns = get_ns('en_ego')

    anchors = soup.find('div', class_='widget mais-lidas').find_all('a')

    for a in anchors:
        title = a['title']
        link = a['href']
        news.append(dict(title=title, link=link))

    return news


def __en_fuxico(soup):
    """
    Gets the most read news from the Fuxico page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Fuxico page
    """
    news = []
    divs = soup.find_all('div', class_='post-news')

    # Limit to 5 news
    i = 0
    for div in divs:
        a = div.find('a', attrs={'class': None})
        if a.span is not None:
            title = a.span.next.next.string
        else:
            title = a.string
        link = 'http://www.ofuxico.com.br' + a['href']
        news.append(dict(title=title, link=link))

        i += 1
        if i == 5:
            break
    return news


def __en_contigo(soup):
    """
    Gets the most read news from the Contigo page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Contigo page
    """
    # DEPRECATED
    news = []
    ns = get_ns('en_contigo')

    anchors = soup.find('div', class_='box mais-lidas clearfix').find_all('a')

    for a in anchors:
        title = a.p.string
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))

    return news


def __en_tititi(soup):
    """
    Gets the most read news from the Tititi page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Tititi page
    """
    # DEPRECATED
    news = []
    ns = get_ns('en_tititi')

    anchors = soup.find('div', class_='box mais-lidas clearfix').find_all('a')

    for a in anchors:
        title = a.p.string
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))

    return news


def __en_vip(soup):
    """
    Gets the most read news from the Área Vip page
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Área Vip page
    """
    news = []

    divs = soup.find_all('div', class_='td-block-span12')

    for d in divs[:3]:
        a = d.find(anchor_has_no_class)
        title = a['title']
        link = a['href']
        news.append(dict(title=title, link=link))

    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(en_ego=__en_ego, en_fuxico=__en_fuxico, en_contigo=__en_contigo, en_tititi=__en_tititi,
                  en_vip=__en_vip, en_om_filmes=__en_om_filmes, en_om_series=__en_om_series, en_om_hqs=__en_om_hqs)


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
