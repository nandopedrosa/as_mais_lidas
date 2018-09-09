"""
views.py: Routing and view rendering of the application


__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import json
from app.aml_utils import getstate, send_email, get_ns
from app.facade import get_most_read
from app.forms import ContactForm
from flask import render_template, request, session, redirect, url_for, jsonify
from flask.ext.babel import gettext
from app import app, babel
from datetime import datetime
from app.aml_config import LANGUAGES

# Default news source
DEFAULT_NS = "uol"


@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    """
    Renders the index (home) page with the default News Source
    :return: The rendered index page
    """
    news, header = get_most_read(DEFAULT_NS)
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

    news, header = get_most_read(p_ns)
    d = dict(news=news, header=header)
    j = json.dumps(d)
    return j


@app.route('/get_local_ns', methods=["GET"])
def get_state():
    """
    Gets the user Local News Source based on their IP Address
    :return: a JSON file with the user State and Local News Source
    """
    state = getstate()

    # DEBUG - Change here to simulate different locations. Comment otherwise.
    # state = 'TO'

    if state == 'notfound':
        ns_title = ''
    else:
        ns_local = get_ns('local' + state)
        ns_title = ns_local.name + '*'

    d = dict(state=state, ns_title=ns_title)
    j = json.dumps(d)
    return j


@app.route('/change_location', methods=["GET"])
def change_location():
    """
    Changes the user Location
    :return: a JSON file with the name of the regional news source based on the new location
    """
    location = request.args.get('location')
    ns_local = get_ns(location)
    ns_name = ns_local.name

    d = dict(ns_name=ns_name)
    j = json.dumps(d)
    return j


@app.route('/send_message', methods=["POST"])
def send_message():
    """
    Sends a contact message
    :return: a JSON file with status code (OK/ERROR). If an error occurs, the JSON file also has a list with the error
    messages and related fields
    """
    form = ContactForm(request.form)

    if form.validate():
        form.errors['error'] = False
        form.errors['status'] = gettext('Message successfully sent')
        send_email(form.name.data, form.email.data, form.message.data)
    else:
        form.errors['status'] = gettext('Your message could not be sent')
        form.errors['error'] = True

    return jsonify(form.errors)


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


# noinspection PyUnusedLocal
@app.errorhandler(404)
def not_found_error(error):
    contact_form = ContactForm()
    current_year = datetime.now().year
    return render_template("404.html",
                           title=gettext('Page not found'),
                           year=current_year,
                           contact_form=contact_form)


# noinspection PyUnusedLocal
@app.errorhandler(500)
def internal_error(error):
    contact_form = ContactForm()
    current_year = datetime.now().year
    return render_template("500.html",
                           title=gettext('Error'),
                           year=current_year,
                           contact_form=contact_form)


@app.route('/error', methods=['GET'])
def ajax_error():
    """
    Handles internal errors that the native Flask Implementation doesn't handle (that is, for AJAX calls)
    :return: The rendered Internal Error Page (500)
    """
    return render_template('500.html'), 500
