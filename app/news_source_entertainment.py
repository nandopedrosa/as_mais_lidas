"""
news_source_entertainment.py: Scraping functions for the most read  News Sources of the Entertainment Category

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app.aml_utils import getpage, parsepage, get_ns, anchor_has_no_class

def __en_nerd(soup):
    """
    Helper function to get Jovem Nerd News
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Jovem Nerd website
    """
    news = []

    links = soup.find('div', class_='highlight-list').find_all('a')

    for a in links:
        link = a['href']
        title = a.string.strip()
        news.append(dict(title=title, link=link))

    return news



def __en_omelete(soup):
    """
    Helper function to get Omelete News
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from a given Omelete Page
    """
    news = []

    anchors = soup.find('aside', class_='c-ranking c-ranking--read').find_all('a')

    for a in anchors:
        link = 'http://www.omelete.com.br' + a['href']
        title = a.find('div', class_='c-ranking__text').string
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
    links = soup.find_all('a', class_='news-box-link')

    # Limit to 10 news
    i = 0
    for link in links:
        title = link.h2.string
        news.append(dict(title=title, link=link['href']))

        i += 1
        if i == 10:
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
                  en_vip=__en_vip, en_omelete=__en_omelete, en_nerd=__en_nerd)


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
