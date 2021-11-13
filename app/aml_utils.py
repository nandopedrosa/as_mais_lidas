"""
util.py: Helper functions and constants common to several News Source operations

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import httplib2
# noinspection PyPackageRequirements
from bs4 import BeautifulSoup
from app import app
from app.decorators import async_decorator
import json
from app.aml_config import SENDGRID_API_KEY
from app.models import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Constants

IP_SERVICE_URL = "http://www.localizaip.com.br/localizar-ip.php?ip=#IP#"

STATES = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
          'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']


def getstate():
    """
    Gets the user State Location based on their IP Address
    :return: State Location (e.g: SP, DF, etc.)
    """
    try:
        # First, we discover the user's public ip address
        response, content = getpage('http://ip.42.pl/raw')  # Download the page
        soup = parsepage(content)  # Then we parse it
        ip = soup.find('body').string

        if ip is None:
            return 'notfound'

        # Now we use some IP localization service to determine from where that IP comes from
        url = IP_SERVICE_URL.replace("#IP#", ip)
        response, content = getpage(url)
        soup = parsepage(content)
        data = soup.find_all('span', class_='style4')[1].get_text()

        state_index = data.find("Estado")

        if state_index != -1:
            start_index = state_index + len("Estado:")
        else:
            return 'notfound'

        end_index = start_index + 2

        state = data[start_index: end_index]

        if state not in STATES:
            state = 'notfound'

        return state
    except Exception:
        return 'notfound'


def getpage(url):
    """
    Downloads the html page

    :rtype: tuple
    :param url: the page address
    :return: the header response and contents (bytes) of the page
    """
    http = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}

    response, content = http.request(url, headers=headers)
    return response, content


def get_outline(url):
    """
    Gets the Outline link for a Paywall URL

    :param url: the original (paywall) page address
    :return: the new url
    """
    if(url is None):
        return ""

    api_base_url = "https://api.outline.com/v3/parse_article?source_url="
    response, content = getpage(api_base_url + url)
    json_content = json.loads(content)
    return "https://outline.com/" + json_content['data']['short_code']


def replace_original_link_with_outline_call(url):
    """
    Replaces the original link with a call to get an outline link

    :param url: the original (paywall) url
    :return: the new url
    """
    return "/outline?original_url=" + url

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


def send_email(username, reply_to, text_body, error_msg=False):
    """
    Sends an email to the given recipients
    :param username: the name of the person who sent the contact message
    :param reply_to: the email of the person who sent the contact message
    :param text_body: the message
    :return: None
    """

    if not error_msg:
        content = '<p>Reply to: ' + reply_to + '</p>' + '<p>' + text_body + '</p>'
        content = content.replace('\r\n', '<br/>')
    else:
        content = text_body

    message = Mail(
        from_email='noreply@asmaislidas.com.br',
        to_emails='fpedrosa@gmail.com',
        subject='[asmaislidas] ' + username + ' has sent you a message',
        html_content=content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

    return response.status_code


def get_ns(key):
    """
    Gets a news_source filtered by key
    :param key: the key of the news source (e.g: g1, uol, etc.)
    :return: the news source object
    """
    ns = NewsSource.query.filter_by(
        key=key).first()  # Fetch news source by key
    return ns
