"""
util.py: Helper functions and constants common to several News Source operations

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import httplib2
# noinspection PyPackageRequirements
from bs4 import BeautifulSoup
from flask.ext.mail import Message
from app import app, mail
from app.decorators import async
from app.aml_config import ADMINS
from app.models import *

# Constants

IP_SERVICE_URL = "http://www.localizaip.com.br/localizar-ip.php?ip=#IP#"

STATES = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
          'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']


def getstate(ip):
    """
    Gets the user State Location based on their IP Address
    :param ip: The user IP
    :return: State Location (e.g: SP, DF, etc.)
    """
    try:
        if ip is None:
            return 'notfound'

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
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}

    response, content = http.request(url, headers=headers)
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


def send_email(username, reply_to, text_body):
    """
    Sends an email to the given recipients
    :param username: the name of the person who sent the contact message
    :param reply_to: the email of the person who sent the contact message
    :param text_body: the message
    :return: None
    """
    subject = '[asmaislidas] {0} has sent you a message'.format(username)
    msg = Message(subject, recipients=ADMINS)
    msg.body = "Name: " + username + "\nReply to: " + reply_to + "\nMessage:\n" + text_body
    __send_email_async(app, msg)


# noinspection PyShadowingNames
@async
def __send_email_async(app, msg):
    """
    Helper function to make send emails asynchronously (there' no point making the user wait for the email to be sent)
    :param app: the flask app
    :param msg: the msg object from Flask Mail
    :return: None
    """
    with app.app_context():
        mail.send(msg)


def get_ns(key):
    """
    Gets a news_source filtered by key
    :param key: the key of the news source (e.g: g1, uol, etc.)
    :return: the news source object
    """
    ns = NewsSource.query.filter_by(key=key).first()  # Fetch news source by key
    return ns
