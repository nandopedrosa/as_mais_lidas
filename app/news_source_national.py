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
    scripts = soup.find_all('script')

    for script in scripts:
        script_content = script.text

        # O conteúdo do G1 agora é gerado por script. Primeiro achamos o script correto, pois são vários
        if script_content.startswith("'use strict'"):
            i = 0

            # Recuperamos as URLs mais acessadas
            while True:
                # Primeiro achamos um top-post (url) com essa chave de busca
                key_index = script_content.find('G1-POST-TOP', i)

                if key_index == -1:
                    break

                # Agora achamos o começo da url
                start_index = script_content.rfind('"', 0, key_index) + 1

                # Agora achamos o final da url
                end_index = script_content.find('"', key_index)

                # E agora pegamos a URL (substring)
                url = script_content[start_index : end_index]

                # Com a URL, entramos na página e descobrimos o título dela
                response, content = getpage(url)
                soup2 = parsepage(content)
                title = soup2.find('h1', class_='content-head__title').string

                news.append(dict(title=title, link=url))

                # Preparamos o próximo índice de busca
                i = key_index + 10

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
    ps = soup.find_all('p', class_='trends-thermometer-description')
    i = 0

    for p in ps:
        if i == 6:  # Six trending topics
            break
        i += 1
        a = p.parent.parent.parent.a
        news.append(dict(title=a['title'], link=a['href']))
    return news


def __folha(soup):
    """
    Gets the most read news from the Folha de Sao Paulo page

    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Folha de Sao Paulo Page
    """
    news = []

    anchors = soup.find('ol', class_='c-most-read__list').find_all('a')

    for a in anchors:
        title = a.string
        link = a['href']
        news.append(dict(title=title, link=link))

    return news


def __bol(soup):
    """
    Gets the most read news from the BOL page

    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the BOL Page
    """
    news = []
    anchors = soup.find('div', class_='mais-clicadas-lista link-primary').find_all('a')

    for a in anchors:
        title = a.find('span', class_='mais-clicadas-item-content').text
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

    links = soup.find('div', id='abril_popular_posts_widget-7').find_all('a', class_='')

    for a in links:
        news.append(dict(title=a.string,
                         link=a['href']))
    return news


def __nexo(soup):
    """
    Gets the most read news from the Jornal Nexo page

    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the Jornal Nexo Page
    """
    news = []

    headers = soup.find('div', class_='news-list top-list').find('div', class_='top-list').find_all('h4')

    for header in headers:
        news.append(dict(title=header.a.text,
                         link=header.a['href']))
    return news


def __local_df(soup):
    """
    Gets the most read news from Distrito Federal Local News (G1 DF)
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from the G1 DF Page
    """
    return __get_local_g1_news(soup)


def __local_sp(soup):
    """
   Gets the most read news from São Paulo Local News (G1 Sao Paulo)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from G1 Sao Paulo page
   """
    return __get_local_g1_news(soup)


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
    # Unordered list
    unordered_list = list(soup.find("img",
                                    src="http://agazetadoacre.com/wp-content/themes/agazeta_do_acre-sembarra/images/mais-lidas-cabec.jpg").parents)[
        5].next_sibling.ul
    list_items = unordered_list.find_all('li')

    for li in list_items:
        title = li.h5.a.string
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

    divs = soup.find_all('div', class_='card-news-small')
    # Incrementer, we only need 4 hits
    i = 0
    for div in divs:
        title = div.find('span', class_='card-news__title')
        news.append(dict(title=title.string, link=ns.url + title.parent['href']))
        i += 1
        if i == 4:
            break
    return news


def __local_ap(soup):
    """
 Gets the most read news from Amapá Local News (Jornal do Dia)
 :param soup: the BeautifulSoup object
 :return: a list with the most read news from Jornal do Dia page
 """
    return __get_local_g1_news(soup)


def __local_am(soup):
    """
   Gets the most read news from Amazonas Local News (Rede Amazonica)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Rede Amazonica page
   """
    return __get_local_g1_news(soup)


def __local_ba(soup):
    """
  Gets the most read news from Bahia Local News (A Tarde)
  :param soup: the BeautifulSoup object
  :return: a list with the most read news from A Tarde page
  """
    news = []
    ns = get_ns('localBA')

    anchors = soup.find('section', class_='maisLidas row').find_all('a')

    for a in anchors:
        title = a.p.string
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
    Gets the most read news from Espirito Santo Local News (TV Gazeta)
    :param soup: the BeautifulSoup object
    :return: a list with the most read news from TV Gazeta page
    """
    return __get_local_g1_news(soup)


def __local_go(soup):
    """
   Gets the most read news from Goiás Local News (TV Anhaguera)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from TV Anhaguera page
   """
    return __get_local_g1_news(soup)


def __local_ma(soup):
    """
   Gets the most read news from Maranhão Local News (Jornal Pequeno)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Jornal Pequeno page
   """
    news = []
    anchors = soup.find('div', id='mais-lidas').find_all('a')

    for a in anchors:
        title = a.string
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
    return __get_local_g1_news(soup)


def __local_mg(soup):
    """
   Gets the most read news from Minas Gerais Local News (Estado de Minas)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Estado de Minas page
   """
    news = []
    anchors = soup.find('ul', class_='list-unstyled list-borded mb-0').find_all('a')

    for a in anchors:
        if a.has_attr('title'):
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
    return __get_local_g1_news(soup)


def __local_pb(soup):
    """
   Gets the most read news from Paraíba Local News (Paraíba Online)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Paraíba Online page
   """
    return __get_local_g1_news(soup)


def __local_pr(soup):
    """
   Gets the most read news from Paraná Local News (Paraná Online)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Paraná Online page
   """
    news = []
    ns = get_ns('localPR')

    anchors = soup.find('div', class_='tbn-coluna col-4 c-mais-lidas-comentadas c-sequencia').find_all('a')

    for a in anchors:
        title = a.string
        link = a['href']
        news.append(dict(title=title, link=link))
    return news


def __local_pi(soup):
    """
   Gets the most read news from Piauí Local News (TV Clube)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from TV Clube page
   """
    return __get_local_g1_news(soup)


def __local_rn(soup):
    """
   Gets the most read news from Rio grande do Norte Local News (Inter TV)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from Inter TV page
   """
    return __get_local_g1_news(soup)


def __local_rs(soup):
    """
   Gets the most read news from Rio Grande do Sul Local News (RBS TV)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from RBS TV page
   """
    return __get_local_g1_news(soup)


def __local_sc(soup):
    """
   Gets the most read news from Santa Catarina Local News (NSC TV)
   :param soup: the BeautifulSoup object
   :return: a list with the most read news from NSC TV page
   """
    return __get_local_g1_news(soup)


def __local_ro(soup):
    """
  Gets the most read news from Rondônia Local News (Rede Amazônica)
  :param soup: the BeautifulSoup object
  :return: a list with the most read news from Rede Amazônica page
  """
    return __get_local_g1_news(soup)


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
    return __get_local_g1_news(soup)


def __get_local_g1_news(soup):
    """
 Gets the most read news from a local G1 news source
 Update: there is no Most Read news from local regions anymore,
 so we just show the first five news
 :param soup: the BeautifulSoup object
 :return: a list with the most read news from a local g1 news source
 """
    news = []
    anchors = soup.find_all('a', class_='feed-post-link gui-color-primary gui-color-hover')

    for a in anchors:
        title = a.string
        link = a['href']
        news.append(dict(title=title, link=link))
    return news


# Strategy Pattern - a dictionary of functions. Key: the name of the News Source. Value: the Function to execute
strategies = dict(g1=__g1, uol=__uol, r7=__r7, folha=__folha, bol=__bol, carta=__carta, veja=__veja, localDF=__local_df,
                  localSP=__local_sp, localRJ=__local_rj, localPE=__local_pe, localAC=__local_ac, localAL=__local_al,
                  localAP=__local_ap, localAM=__local_am, localBA=__local_ba, localCE=__local_ce, localES=__local_es,
                  localGO=__local_go, localMA=__local_ma, localMT=__local_mt, localMS=__local_ms, localMG=__local_mg,
                  localPA=__local_pa, localPB=__local_pb, localPR=__local_pr, localPI=__local_pi, localRN=__local_rn,
                  localRS=__local_rs, localSC=__local_sc, localRO=__local_ro, localRR=__local_rr, localSE=__local_se,
                  localTO=__local_to, nexo=__nexo)


def get_most_read(key):
    """
    Gets the most read news from a given page

    :param key: the key of the source page (e.g: g1)
    :return: a list with the most read news from the page and the name of news source
    """
    ns = get_ns(key)

    if key == 'localAP':
        ns.url = 'http://g1.globo.com/ap/amapa/'
    elif key == 'localPB':
        ns.url = 'http://g1.globo.com/pb/paraiba/'
    elif key == 'localSC':
        ns.url = 'http://g1.globo.com/sc/santa-catarina/'

    response, content = getpage(ns.url)  # Download the page
    soup = parsepage(content)  # Then we parse it
    strategy = strategies[key]  # Then we execute the selected Strategy based on the source
    return strategy(soup), ns.name
