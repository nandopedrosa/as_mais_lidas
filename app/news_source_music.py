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

    anchors = soup.find('ol', class_='c-trending__list').find_all('a')

    for a in anchors:
        title = a.text
        link = a['href']
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

    paragraphs = soup.find_all('p', class_='linkManchete')
    i = 0;

    for p in paragraphs:
        title = p.string
        link = p.a['href']
        news.append(dict(title=title, link=link))
        i += 1
        if i == 10:
            break

    return news

def __m_rockbizz(soup):
    """
   Gets the most read news from the Rock Bizz page
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from the Rock Bizz page
   """
    news = []
    ns = get_ns('m_bizz')

    section = soup.find('section', id='recent-posts-2')
    items = section.find_all('li')

    for item in items:
        title = item.text
        link = item.a['href']
        news.append(dict(title=title, link=link))   

    return news    


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(m_rs=__m_rs, m_bizz=__m_rockbizz)


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
