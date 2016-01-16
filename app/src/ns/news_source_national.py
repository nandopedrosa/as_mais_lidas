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
        news.append(dict(title=a.string,
                         link=util.urls['veja'] + a['href']))  # Relative link, we have to prefix with the page domain
    return news


def __local_df(soup):
    """
    Gets the most read news from Distrito Federal Local News (Correio Braziliense)
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
    Gets the most read news from Sao Paulo Local News (Estadao)
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


def __local_pe(soup):
    """
    Gets the most read news from Pernambuco Local News (JC Online)
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from JC Online Page
    """
    news = []
    list_items = soup.find('div', class_='maisVistas').find_all('li', class_='texto')

    for li in list_items:
        title = li.a.string
        link = li.a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_ac(soup):
    """
   Gets the most read news from Acre Local News (Gazeta do Acre)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Gazeta do Acre page
   """
    news = []
    list_items = soup.find('div', id='direita_').find_all('li')

    for li in list_items:
        title = li.a.string
        link = li.a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_al(soup):
    """
  Gets the most read news from Alagoas Local News (Cada Minuto)
  :param soup: the BeautifulSoup object
  :return: a list with the most read news from Cada Minuto page
  """
    news = []
    links = soup.find('ul', class_='read-more').find_all('a')

    for a in links:
        news.append(dict(title=a.h3.string, link=util.urls['localAL'] + a['href']))
    return news


def __local_ap(soup):
    """
 Gets the most read news from Amapá Local News (Jornal do Dia)
 :param soup: the BeautifulSoup object
 :return: a list with the most read news from Jornal do Dia page
 """
    news = []
    list_items = soup.find('div', id='Mod212').find_all('li')

    for li in list_items:
        title = li.h4.a.string
        link = li.h4.a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_am(soup):
    """
 Gets the most read news from Amazonia Local News (A Crítica)
 :param soup: the BeautifulSoup object
 :return: a list with the most read news from A Crítica page
 """
    news = []
    list_items = soup.find('div', id='mas-leidas').find_all('li')

    for li in list_items:
        title = li.a.string
        link = util.urls['localAM'] + li.a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_ba(soup):
    """
  Gets the most read news from Bahia Local News (A Tarde)
  :param soup: the BeautifulSoup object
  :return: a list with the most read news from A Tarde page
  """
    news = []
    anchors = soup.find('aside', id='conteudos').find_all('a')

    for a in anchors:
        title = a.string
        link = util.urls['localBA'] + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_ce(soup):
    """
    Gets the most read news from Ceará Local News (Diário do Nordeste)
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from Diário do Nordeste page
    """
    news = []
    anchors = soup.find('section', id='mais-lidas').find_all('a')

    for a in anchors:
        title = a.string
        link = util.urls['localCE'] + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_es(soup):
    """
   Gets the most read news from Espírito Santo Local News (Folha Vitória)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Folha Vitória page
   """
    news = []
    list_items = soup.find('div', class_='readMore container t2').find_all('li', class_='geral')

    for li in list_items:
        title = li.a.string
        link = util.urls['localES'] + li.a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_go(soup):
    """
   Gets the most read news from Goiás Local News (TV Anhaguera)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from TV Anhaguera page
   """
    news = []
    anchors = soup.find('div', class_='widget widget-mais-lidas').find_all('a')

    for a in anchors:
        title = a.string
        link = "http://g1.globo.com" + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_ma(soup):
    """
   Gets the most read news from Maranhão Local News (Jornal Pequeno)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Jornal Pequeno page
   """
    news = []
    anchors = soup.find('div', class_='tablidas tab').find_all('a')

    for a in anchors:
        title = a.h5.string
        link = a['href']
        news.append(dict(title=title, link=link))
    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(g1=__g1, uol=__uol, r7=__r7, folha=__folha, bol=__bol, carta=__carta, veja=__veja, localDF=__local_df,
                  localSP=__local_sp, localRJ=__local_rj, localPE=__local_pe, localAC=__local_ac, localAL=__local_al,
                  localAP=__local_ap, localAM=__local_am, localBA=__local_ba, localCE=__local_ce, localES=__local_es,
                  localGO=__local_go, localMA=__local_ma)


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
