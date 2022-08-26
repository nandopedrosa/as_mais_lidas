"""
views.py: Routing and view rendering of the application


__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import json
from app.aml_utils import get_outline
from app.facade import get_most_read
from datetime import datetime
from flask import render_template, request, session, redirect
from app import app
import traceback


@app.route('/most_read_ns', methods=["GET"])
def ns():
    """
    Gets the most read news from a specific news source
    If the request parameters contains Local information, we fetch data from the Local News Source
    :return: a JSON file with the news list
    """
    p_ns = request.args.get('ns') 
    news, header = get_most_read(p_ns)
    d = dict(news=news, header=header)
    j = json.dumps(d)
    return j

@app.route('/outline', methods=["GET"])
def outline():
    """
    Gets the outline page of a given Paywall URL    
    :return the outline page
    """
    original_url = request.args.get('original_url')
    outline_url = get_outline(original_url)    
    return redirect(outline_url)

# noinspection PyUnusedLocal
@app.errorhandler(404)
def not_found_error(error):
    current_year = datetime.now().year
    return render_template("404.html",
                           title='Página não encontrada',
                           year=current_year,
                           )


# noinspection PyUnusedLocal
@app.errorhandler(500)
def internal_error(error):
    current_year = datetime.now().year
    stack_trace_msg = traceback.format_exc()
    return render_template("500.html",
                           title='Ooops')
                           


@app.route('/error', methods=['GET'])
def ajax_error():
    """
    Handles internal errors that the native Flask Implementation doesn't handle (that is, for AJAX calls)
    :return: The rendered Internal Error Page (500)
    """
    return render_template('500.html'), 500
