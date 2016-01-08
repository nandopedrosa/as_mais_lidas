"""
util.py: Helper functions and constants common to several News Source operations

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import httplib2
from bs4 import BeautifulSoup

# Constants

IP_SERVICE_URL = "http://www.localizaip.com.br/localizar-ip.php?ip=#IP#"

STATES = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
          'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

# Used for the Menu of News Sources
STATES_NS = dict(AC='not applicable', AL='not applicable', AP='not applicable', AM='not applicable',
                 BA='not applicable', CE='not applicable', DF='Correio Braziliense', ES='not applicable',
                 GO='not applicable', MA='not applicable', MT='not applicable', MS='not applicable',
                 MG='not applicable', PA='not applicable', PB='not applicable', PR='not applicable',
                 PE='JC Online', PI='not applicable', RJ='O Globo', RN='not applicable',
                 RS='not applicable', RO='not applicable', RR='not applicable', SC='not applicable',
                 SP='Estadão', SE='not applicable', TO='not applicable')

# Used in BeautifulSoup
urls = dict(g1="http://g1.globo.com/index.html", uol="http://www.uol.com.br/", r7="http://www.r7.com/",
            folha='http://www.folha.uol.com.br/', bol="http://www.bol.uol.com.br/",
            carta="http://www.cartacapital.com.br/", veja="http://veja.abril.com.br/",
            localDF="http://www.correiobraziliense.com.br/", localSP="http://www.estadao.com.br/",
            localRJ="http://oglobo.globo.com/rio/", localPE="http://jconline.ne10.uol.com.br/")

# Used for the header of the main panel
friendly_names = dict(g1="G1 (g1.globo.com)", uol="UOL (www.uol.com.br)", r7="R7 (www.r7.com)",
                      folha='Folha de São Paulo (www.folha.uol.com.br)', bol="BOL (www.bol.uol.com.br)",
                      carta="Carta Capital (www.cartacapital.com.br)", veja="Veja (veja.abril.com.br)",
                      localDF="Correio Braziliense (www.correiobraziliense.com.br)",
                      localSP="Estadão (www.estadao.com.br)", localPE="JC Online (jconline.ne10.uol.com.br)",
                      localRJ="O Globo (oglobo.globo.com/rio)")


# End of Constants


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
