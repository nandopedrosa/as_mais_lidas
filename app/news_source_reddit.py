"""
news_source_reddit.py: Scraping functions for the most read  News Sources of the Reddit Category

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app.aml_utils import getpage, parsepage, get_ns


def __re_any(soup):
    """
    Gets the most read entries of the Ask Reddit/TIL/IAmA  subreddits from the last 24 hours
    :param soup: the BeautifulSoup object
    :param is_iama: indicates if we want the IAmA page, in which case we ignore the requests
    :return: a list with the most read news from the Ask Reddit page
    """
    news = []

    entries = soup.find('div', id='siteTable').find_all('div', class_='thing')

    i = 0

    for entry in entries:
        title = entry.find('p', class_='title').a.string
        # Ignore Requests
        if 'AMA Request' in title:
            continue
        link = entry.find('a', class_='bylink comments may-blank')['href']
        news.append(dict(title=title, link=link))
        i += 1
        if i == 5:
            break

    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(re_ask=__re_any, re_til=__re_any, re_iama=__re_any)


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
