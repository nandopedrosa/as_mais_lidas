"""
news_source_national.py: Scraping functions for the most read National News Sources

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import html
from app.aml_utils import getpage, anchor_has_no_class, parsepage, get_ns
from app.models import *
from app import db


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
    container = soup.select('.mais_lidas')[0]
    most_read = container.find_all('a', class_='text')

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
    anchors = soup.find('ul', class_='maisclicadas').find_all('a')

    for a in anchors:
        title = a.span.string.next
        link = a['href']
        news.append(dict(title=title, link=link))
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
    ns = get_ns('veja')

    links = soup.find('div', class_='mais-lidas').find('ul').find_all(anchor_has_no_class)
    links_remainder = soup.find('div', class_='mais-lidas').find('ul').next_sibling.find_all(anchor_has_no_class)
    links.extend(links_remainder)

    for a in links:
        news.append(dict(title=a.string,
                         link=ns.url + a['href']))  # Relative link, we have to prefix with the page domain
    return news


def __local_df(soup):
    """
    Gets the most read news from Distrito Federal Local News (G1 DF)
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the G1 DF Page
    """
    news = []
    anchors = soup.find('ul', class_='highlights').find_all('a')

    for a in anchors:
        title = a.span.string.strip()
        link = a['href']
        news.append(dict(title=title, link=link))
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
    ns = get_ns('localAL')

    links = soup.find('ul', class_='read-more').find_all('a')

    for a in links:
        news.append(dict(title=a.h3.string, link=ns.url + a['href']))
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
    ns = get_ns('localAM')

    list_items = soup.find('div', id='mas-leidas').find_all('li')

    for li in list_items:
        title = li.a.string
        link = ns.url + li.a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_ba(soup):
    """
  Gets the most read news from Bahia Local News (A Tarde)
  :param soup: the BeautifulSoup object
  :return: a list with the most read news from A Tarde page
  """
    news = []
    ns = get_ns('localBA')

    anchors = soup.find('aside', id='conteudos').find_all('a')

    for a in anchors:
        title = a.string
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_ce(soup):
    """
    Gets the most read news from Ceará Local News (Diário do Nordeste)
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from Diário do Nordeste page
    """
    news = []
    ns = get_ns('localCE')

    anchors = soup.find('section', id='mais-lidas').find_all('a')

    for a in anchors:
        title = a.string
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_es(soup):
    """
   Gets the most read news from Espírito Santo Local News (Folha Vitória)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Folha Vitória page
   """
    news = []
    ns = get_ns('localES')

    list_items = soup.find('div', class_='readMore container t2').find_all('li', class_='geral')

    for li in list_items:
        title = li.a.string
        link = ns.url + li.a['href']
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
        title = a['title']
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


def __local_mt(soup):
    """
   Gets the most read news from Mato Grosso Local News (Gazeta Digital)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Gazeta Digital page
   """
    news = []
    ns = get_ns('localMT')

    anchors = soup.find_all('a', class_='top10titulo')

    for a in anchors:
        title = a.string
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_ms(soup):
    """
   Gets the most read news from Mato Grosso do Sul Local News (TV Morena)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from TV Morena page
   """
    news = []
    anchors = soup.find('div', class_='widget widget-mais-lidas').find_all('a')

    for a in anchors:
        title = a['title']
        link = "http://g1.globo.com" + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_mg(soup):
    """
   Gets the most read news from Minas Gerais Local News (Estado de Minas)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Estado de Minas page
   """
    news = []
    anchors = soup.find('div', id='lidas').find_all('a')

    for a in anchors:
        title = a['title']
        link = a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_pa(soup):
    """
   Gets the most read news from Pará Local News (Rede Liberal)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Rede Liberal page
   """
    news = []
    anchors = soup.find('div', class_='widget widget-mais-lidas').find_all('a')

    for a in anchors:
        title = a['title']
        link = "http://g1.globo.com" + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_pb(soup):
    """
   Gets the most read news from Paraíba Local News (Paraíba Online)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Paraíba Online page
   """
    news = []
    anchors = soup.find('div', class_='timeline amarelo').find_all('a')

    for a in anchors:
        title = a.string
        link = a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_pr(soup):
    """
   Gets the most read news from Paraná Local News (Paraná Online)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Paraná Online page
   """
    news = []
    ns = get_ns('localPR')

    anchors = soup.find('ul', id='lidas').find_all('a')

    for a in anchors:
        title = a.string
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_pi(soup):
    """
   Gets the most read news from Piauí Local News (TV Clube)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from TV Clube page
   """
    news = []
    anchors = soup.find('div', class_='widget widget-mais-lidas').find_all('a')

    for a in anchors:
        title = a['title']
        link = "http://g1.globo.com" + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_rn(soup):
    """
   Gets the most read news from Rio grande do Norte Local News (Inter TV)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Inter TV page
   """
    news = []
    anchors = soup.find('div', class_='widget widget-mais-lidas').find_all('a')

    for a in anchors:
        title = a['title']
        link = "http://g1.globo.com" + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_rs(soup):
    """
   Gets the most read news from Rio Grande do Sul Local News (RBS TV)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from RBS TV page
   """
    news = []
    anchors = soup.find('div', class_='widget widget-mais-lidas').find_all('a')

    for a in anchors:
        title = a['title']
        link = "http://g1.globo.com" + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_sc(soup):
    """
   Gets the most read news from Santa Catarina Local News (Click RBS)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Click RBS page
   """
    news = []
    anchors = soup.find('div', id='noticiasmaislidas').find_all('a')

    for a in anchors:
        title = a.string
        link = a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_ro(soup):
    """
   Gets the most read news from Rondônia Local News (Rondonia ao Vivo)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Rondonia ao Vivo page
   """
    news = []
    ns = get_ns('localRO')

    anchors = soup.find('div', id='mais-lidas').find_all('a', class_='fill-lidas')

    for a in anchors:
        title = a['title']
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_rr(soup):
    """
   Gets the most read news from Roraima Local News (Folha de Boa Vista)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Folha de Boa Vista page
   """
    news = []
    ns = get_ns('localRR')

    divs = soup.find('div', class_='mais-lidas').find_all('div', class_="ultimas-text")

    for div in divs:
        a = div.find('a')
        title = a.string
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_se(soup):
    """
   Gets the most read news from Sergipe Local News (Jornal do Dia)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Jornal do Dia page
   """
    news = []
    ns = get_ns('localSE')

    anchors = soup.find('div', class_='coluna3 bordaTopoCinza').find_all('a')

    for a in anchors:
        title = a.string
        link = ns.url + a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_to(soup):
    """
   Gets the most read news from Tocantins Local News (TV Anhaguera)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from TV Anhaguera page
   """
    news = []
    anchors = soup.find('div', class_='widget widget-mais-lidas').find_all('a')

    for a in anchors:
        title = a['title']
        link = "http://g1.globo.com" + a['href']
        news.append(dict(title=title, link=link))
    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(g1=__g1, uol=__uol, r7=__r7, folha=__folha, bol=__bol, carta=__carta, veja=__veja, localDF=__local_df,
                  localSP=__local_sp, localRJ=__local_rj, localPE=__local_pe, localAC=__local_ac, localAL=__local_al,
                  localAP=__local_ap, localAM=__local_am, localBA=__local_ba, localCE=__local_ce, localES=__local_es,
                  localGO=__local_go, localMA=__local_ma, localMT=__local_mt, localMS=__local_ms, localMG=__local_mg,
                  localPA=__local_pa, localPB=__local_pb, localPR=__local_pr, localPI=__local_pi, localRN=__local_rn,
                  localRS=__local_rs, localSC=__local_sc, localRO=__local_ro, localRR=__local_rr, localSE=__local_se,
                  localTO=__local_to)


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
