"""
views.py: Routing and view rendering of the application

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import json
import util
import facade
from forms import ContactForm
from flask import render_template, request, session, redirect, url_for
from flask.ext.babel import gettext
from app import app, babel
from datetime import datetime
from config import LANGUAGES

# Default news source
DEFAULT_NS = "uol"


@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    """
    Renders the index (home) page with the default News Source
    :return: The rendered index page
    """
    news, header = facade.get_most_read(DEFAULT_NS)
    current_year = datetime.now().year
    contact_form = ContactForm()
    return render_template("ns.html",
                           title=gettext('Home Page'),
                           year=current_year,
                           news=news,
                           header=header,
                           contact_form=contact_form)


@app.route('/most_read_ns', methods=["GET"])
def ns():
    """
    Gets the most read news from a specific news source
    If the request parameters contains Local information, we fetch data from the Local News Source
    :return: a JSON file with the news list
    """
    p_ns = request.args.get('ns')
    p_state = request.args.get('local')

    if p_state:
        p_ns += p_state  # eg.: localDF, localSP, etc.

    news, header = facade.get_most_read(p_ns)
    d = dict(news=news, header=header)
    j = json.dumps(d)
    return j


@app.route('/get_local_ns', methods=["GET"])
def get_state():
    """
    Gets the user Local News Source based on their IP Address
    :return: a JSON file with the user State and Local News Source
    """
    ip = request.args.get('ip')

    state = util.getstate(ip)

    # DEBUG - Change here to simulate different locations. Comment otherwise.
    # state = 'TO'

    if state == 'notfound':
        ns_title = ''
    else:
        ns_title = util.STATES_NS[state] + '*'

    d = dict(state=state, ns_title=ns_title)
    j = json.dumps(d)
    return j


@app.route('/change_location', methods=["GET"])
def change_location():
    """
    Changes the user Location
    :return: a JSON file with the name of the regional news source based on the new location
    and the location ID (e.g: localAC)
    """
    location = request.args.get('location')
    ns_name = util.friendly_names[location]

    d = dict(ns_name=ns_name)
    j = json.dumps(d)
    return j


@app.route('/send_message', methods=["POST"])
def send_message():
    """
    Sends a contact message
    :return: a JSON file with status code (OK/ERRO  R). If an error occurs, the JSON file also has a list with the error
    messages and related fields
    """
    form = ContactForm(request.form)

    if form.validate():
        form.errors['error'] = False
        util.send_email(form.name.data, form.email.data, form.message.data)
    else:
        form.errors['error'] = True

    return json.dumps(form.errors)


@app.route('/lang/<code>', methods=['POST'])
def lang(code):
    """
    Changes the language of the app for a given session
    :param code: the language code (e.g: pt-BR)
    :return: just a generic String (it is mandatory to return something in route functions)
    """
    if code in LANGUAGES:
        session['lang'] = code

    return 'Changed language to: ' + code


@babel.localeselector
def get_locale():
    """
    Gets the current language for the application
    :return: the current language
    """
    if 'lang' in session:
        return session['lang']
    else:
        return 'pt'


