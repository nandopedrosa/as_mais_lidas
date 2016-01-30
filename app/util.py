"""
util.py: Helper functions and constants common to several News Source operations

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import httplib2
from bs4 import BeautifulSoup
from app import app
from app import mail

# Constants

IP_SERVICE_URL = "http://www.localizaip.com.br/localizar-ip.php?ip=#IP#"

STATES = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
          'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

# Used for the Menu of News Sources
STATES_NS = dict(AC='Gazeta do Acre', AL='Cada Minuto', AP='Jornal do Dia', AM='A Crítica',
                 BA='A Tarde', CE='Diário do Nordeste', DF='Correio Braziliense', ES='Folha Vitória',
                 GO='TV Anhaguera', MA='Jornal Pequeno', MT='Gazeta Digital', MS='TV Morena',
                 MG='Estado de Minas', PA='Rede Liberal', PB='Paraíba Online', PR='Paraná Online',
                 PE='JC Online', PI='TV Clube', RJ='O Globo', RN='Inter TV',
                 RS='RBS TV', RO='Rondônia ao Vivo', RR='Folha de Boa Vista', SC='Click RBS',
                 SP='Estadão', SE='Jornal do Dia', TO='TV Anhaguera')

# Used in BeautifulSoup
urls = dict(g1="http://g1.globo.com/index.html", uol="http://www.uol.com.br/", r7="http://www.r7.com/",
            folha='http://www.folha.uol.com.br/', bol="http://www.bol.uol.com.br/",
            carta="http://www.cartacapital.com.br/", veja="http://veja.abril.com.br",
            localDF="http://www.correiobraziliense.com.br/", localSP="http://www.estadao.com.br/",
            localRJ="http://oglobo.globo.com/rio/", localPE="http://jconline.ne10.uol.com.br/",
            localAC="http://agazetadoacre.com/noticias/", localAL="http://www.cadaminuto.com.br/",
            localAP="http://www.jdia.com.br/portal2/", localAM="http://acritica.uol.com.br",
            localBA="http://atarde.uol.com.br", localCE="http://diariodonordeste.verdesmares.com.br",
            localES="http://www.folhavitoria.com.br", localGO="http://g1.globo.com/goias/",
            localMA="http://jornalpequeno.com.br/", localMT="http://www.gazetadigital.com.br",
            localMS="http://g1.globo.com/ms", localMG="http://www.em.com.br/",
            localPA="http://g1.globo.com/pa/para/", localPB="http://paraibaonline.net.br/",
            localPR="http://www.parana-online.com.br", localPI="http://g1.globo.com/pi/",
            localRN="http://g1.globo.com/rn/", localRS="http://g1.globo.com/rs/rio-grande-do-sul/index.html",
            localSC="http://www.clicrbs.com.br/sc/", localRO="http://www.rondoniaovivo.com",
            localRR="http://www.folhabv.com.br/", localSE="http://www.jornaldodiase.com.br/",
            localTO="http://g1.globo.com/to", ny="http://www.nytimes.com/most-popular",
            wp="http://www.washingtonpost.com/", tg="http://www.theguardian.com/international",
            lf="http://www.lefigaro.fr/", tt="http://www.telegraph.co.uk", ep="http://elpais.com/")

# Used for the header of the main panel
friendly_names = dict(g1="G1", uol="UOL", r7="R7",
                      folha='Folha de São Paulo', bol="BOL",
                      carta="Carta Capital", veja="Veja",
                      localDF="Correio Braziliense",
                      localSP="Estadão", localPE="JC Online",
                      localRJ="O Globo", localAL="Cada Minuto",
                      localAC="A Gazeta do Acre",
                      localAP="Jornal do Dia", localAM="A Crítica",
                      localBA="A Tarde",
                      localCE="Diário do Nordeste",
                      localES="Folha Vitória", localGO="TV Anhaguera",
                      localMA="Jornal Pequeno",
                      localMT="Gazeta Digital",
                      localMS="TV Morena",
                      localMG="Estado de Minas", localPA="Rede Liberal",
                      localPB="Paraíba Online",
                      localPR="Paraná Online (www.parana-online.com.br/)", localPI="TV Clube",
                      localRN="Inter TV", localRS="RBS TV",
                      localSC="Click RBS", localRO="Rondônia ao Vivo",
                      localRR="Folha de Boa Vista",
                      localSE="Jornal do Dia", localTO="TV Anhaguera",
                      ny="NY Times", wp="Washington Post",
                      tg="The Guardian", lf="Le Figaro",
                      tt="The Telegraph", ep="El País")


def getstate(ip):
    """
    Gets the user State Location based on their IP Address
    :param ip: The user IP
    :return: State Location (e.g: SP, DF, etc.)
    """
    url = IP_SERVICE_URL.replace("#IP#", ip)
    response, content = getpage(url)
    soup = parsepage(content)
    data = soup.find_all('span', class_='style4')[3].get_text()

    start_index = data.index("Estado:") + len("Estado:")
    end_index = start_index + 2
    state = data[start_index: end_index]

    if state not in STATES:
        state = 'notfound'

    return state


def getpage(url):
    """
    Downloads the html page

    :rtype: tuple
    :param url: the page address
    :return: the header response and contents (bytes) of the page
    """
    http = httplib2.Http('.cache')
    response, content = http.request(url, headers={'User-agent': 'Mozilla/5.0'})
    return response, content


def parsepage(content):
    """
    Parses a single page and its contents into a BeautifulSoup object

    :param content: bytearray
    :return soup: object
    """
    soup = BeautifulSoup(content, 'lxml')
    return soup


def anchor_has_no_class(tag):
    """
    Helper function. Checks if an anchor tag has class attribute

    :param tag: an HTML tag
    :return: boolean value
    """
    return not tag.has_attr('class') and tag.name == 'a'
