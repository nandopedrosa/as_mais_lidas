"""
news_source_international.py: Scraping functions for the most read International News Sources

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import util


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
    headers = soup.find('div', id='div-SHARED').find_all('h3', class_='topFiveComment')

    for h in headers:
        a = h.find('a')
        link = util.urls['tt'] + a['href']
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
        title = 'not-found'

        # Sometimes the item has a Span element (Video icon), sometimes it doesn't
        span = a.find('span')
        if span is None:
            title = a.string
        else:
            title = span.next_sibling.string

        news.append(dict(title=title, link=link))
    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(ny=__ny, wp=__wp, tg=__tg, lf=__lf, tt=__tt, ep=__ep)


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
