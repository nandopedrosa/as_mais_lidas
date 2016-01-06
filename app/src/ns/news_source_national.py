"""
news_source_national.py: Scraping functions for the most read National News Sources

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import html
from src.utils import util


def __g1(soup):
    """
    Gets the most read news from the g1 page

    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the G1 Page
    """
    news = []
    container = soup.select('ul.highlights > li')

    for item in container:
        news.append(dict(title=item.a.span.string, link=item.a['href']))
    return news


def __uol(soup):
    """
    Gets the most read news from the UOL page

    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the UOL Page
    """
    news = []
    container = soup.select('.mais-lidas-container')[0]
    most_read = container.find_all('li')

    for item in most_read:
        title = item.find('span', class_='cor-transition').get_text()
        news.append(dict(title=title, link=item.a['href']))
    return news


def __r7(soup):
    """
    Gets the most read news from the R7 page

    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the R7 Page
    """
    news = []
    container = soup.select('.most-read')[0]
    most_read = container.find_all('a')

    for item in most_read:
        news.append(dict(title=item.string, link=item['href']))
    return news


def __folha(soup):
    """
    Gets the most read news from the Folha de Sao Paulo page

    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Folha de Sao Paulo Page
    """
    news = []

    # We have to get the data from a script tag and process the raw text...
    data = soup.select('#folha-top')[0].next_sibling.next_sibling.string

    # Line by line...
    lines = data.split('\n')

    # For each line...
    for i, line in enumerate(lines):
        # If we reach the end of the array, we break from the loop
        if "]" in line:
            break

        if line.strip().startswith('title'):
            # We get the title and the link of the news
            title = __folha_get_script_content(line, is_title=True)
            link = __folha_get_script_content(lines[i + 1])
            news.append(dict(title=title, link=link))

    return news


def __folha_get_script_content(line, is_title=False):
    """
    Processes the Folha de São Paulo script lines to get the Title and Link of the most read news
    :param line:  a line from the script
    :return: title or link
    """
    start_index = line.index('"') + 1
    last_index = line.rindex('"')
    content = line[start_index:last_index]

    # We have to escape html entities for the Title content
    if is_title:
        content = html.unescape(content)
        content = content.replace("\;", "")  # Unescape still leaves some garbage we have to clean...

    return content


def __bol(soup):
    """
    Gets the most read news from the BOL page

    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the BOL Page
    """
    news = []
    container = soup.find('ul', class_='maisclicadas')
    most_read = container.find_all('li')

    for item in most_read:
        news.append(dict(title=item.a.span.next_element.next_element, link=item.a['href']))
    return news


def __carta(soup):
    """
    Gets the most read news from the Carta Capital page

    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Carta Capital Page
    """
    news = []
    container = soup.find('dd', id='fieldset-maisacessadas-semana')
    most_read = container.find_all('li')

    for item in most_read:
        news.append(dict(title=item.a.string, link=item.a['href']))
    return news


def __veja(soup):
    """
    Gets the most read news from the Veja page

    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Veja Page
    """
    news = []

    links = soup.find('div', class_='mais-lidas').find('ul').find_all(util.anchor_has_no_class)
    links_remainder = soup.find('div', class_='mais-lidas').find('ul').next_sibling.find_all(util.anchor_has_no_class)
    links.extend(links_remainder)

    for a in links:
        news.append(dict(title=a.string, link=a['href']))
    return news


def __local_df(soup):
    """
    Gets the most read news from the Distrito Federal Local News (Correio Braziliense)
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Correio Braziliense Page
    """
    news = []
    container = soup.find('div', id='lidas')
    links = container.find_all('a')

    for a in links:
        news.append(dict(title=a['title'], link=a['href']))
    return news


def __local_sp(soup):
    """
    Gets the most read news from the Sao Paulo Local News (Estadao)
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Estadao Page
    """
    news = []
    container = soup.find('ul', id='lidas')
    links = container.find_all('a')

    for a in links:
        news.append(dict(title=a.p.string, link=a['href']))
    return news


def __local_rj(soup):
    """
    Gets the most read news from the Rio de Janeiro Local News (O Globo)
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from O Globo Page
    """
    news = []
    container = soup.find('div', id='lidas')
    links = container.find_all('a')

    for a in links:
        news.append(dict(title=a.string, link=a['href']))
    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(g1=__g1, uol=__uol, r7=__r7, folha=__folha, bol=__bol, carta=__carta, veja=__veja, localDF=__local_df,
                  localSP=__local_sp, localRJ=__local_rj)


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
