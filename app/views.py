"""
views.py: Routing and view rendering of the application

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import json
from flask import render_template, request
from app import app
import src.utils.util as util
import src.facade as facade

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
    return render_template("ns.html",
                           title="Home",
                           news=news,
                           header=header)


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
    state = 'PI'

    if state == 'notfound':
        ns_title = ''
    else:
        ns_title = util.STATES_NS[state] + '*'

    d = dict(state=state, ns_title=ns_title)
    j = json.dumps(d)
    return j
