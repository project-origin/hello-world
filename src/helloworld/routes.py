import requests
import urllib.parse
from flask import request, render_template, redirect, url_for, make_response, session

from helloworld.auth import register_login_state, fetch_token, parse_id_token
from helloworld.settings import (
    PROJECT_URL,
    OAUTH2_LOGOUT_ENDPOINT,
    DATAHUB_SERVICE_URL,
    ACCOUNT_SERVICE_URL,
)


def index():
    """
    Displays a Log in-link if user is not logged in.
    Displays a menu if user is logged in.
    """
    env = {
        'logged_in': session.get('logged_in', False),
        'name': session.get('name'),
    }

    return render_template('index.html', **env)


def login():
    """
    Redirects user to login page.
    """
    login_url, login_state = register_login_state()

    return redirect(login_url)


def login_callback():
    """
    User is redirected to this endpoint upon returning from login flow.
    """
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    scopes = request.args.get('scopes', '').split(' ')

    if error:
        raise Exception(error)

    # Fetch token
    token = fetch_token(code, state)
    id_token = parse_id_token(token['id_token'])

    # No id_token means the user declined to give consent
    if id_token is not None:
        session['login_state'] = None
        session['logged_in'] = True
        session['subject'] = id_token['sub']
        session['name'] = id_token['name']
        session['token'] = token['access_token']

    return redirect(url_for('index'))


def logout():
    """
    Logs out the user by clearing sessions and redirecting to logout flow.
    """
    session['login_state'] = None
    session['logged_in'] = None
    session['subject'] = None
    session['name'] = None
    session['token'] = None

    return redirect('%s?post_logout_redirect_uri=%s' % (
        OAUTH2_LOGOUT_ENDPOINT,
        urllib.parse.quote(PROJECT_URL),
    ))


def show_measurement_list():
    """
    Shows a list of 50 arbitrary measurements (without filters).

    Endpoint docs:
    """
    response = requests.post(
        url=f'{DATAHUB_SERVICE_URL}/measurements',
        headers={'Authorization': 'Bearer %s' % session['token']},
        verify=False,
        json={
            'offset': 0,
            'limit': 50,
            'filters': {},
        },
    )

    response_json = response.json()

    env = {
        'measurements': response_json['measurements'],
    }

    return render_template('measurement-list.html', **env)


def show_measurement_summary():
    """
    Shows a summary of measurements with a 1-day resolution.
    Values are grouped by GSRN number.

    Endpoint docs:
    """
    response = requests.post(
        url=f'{DATAHUB_SERVICE_URL}/measurements/summary',
        headers={'Authorization': 'Bearer %s' % session['token']},
        verify=False,
        json={
            'resolution': 'day',
            'grouping': ['gsrn'],
            'fill': False,
            'filters': {},
        },
    )

    response_json = response.json()

    env = {
        'labels': response_json['labels'],
        'groups': response_json['groups'],
    }

    return render_template('measurement-summary.html', **env)


def show_ggo_list():
    """
    Shows a list of 50 arbitrary GGOs (without filters).

    Endpoint docs:
    """
    response = requests.post(
        url=f'{ACCOUNT_SERVICE_URL}/ggo',
        headers={'Authorization': 'Bearer %s' % session['token']},
        verify=False,
        json={
            'offset': 0,
            'limit': 50,
            'filters': {},
        },
    )

    response_json = response.json()

    env = {
        'ggos': response_json['results'],
    }

    return render_template('ggo-list.html', **env)


def show_ggo_summary():
    """
    Shows a summary of GGOs with a 1-day resolution.
    Values are grouped by sector (price area).

    Endpoint docs:
    """
    response = requests.post(
        url=f'{ACCOUNT_SERVICE_URL}/ggo/summary',
        headers={'Authorization': 'Bearer %s' % session['token']},
        verify=False,
        json={
            'resolution': 'day',
            'grouping': ['sector'],
            'fill': True,
            'filters': {},
        },
    )

    response_json = response.json()

    env = {
        'labels': response_json['labels'],
        'groups': response_json['groups'],
    }

    return render_template('ggo-summary.html', **env)


def show_environment_declaration():
    """
    Shows emission data for one or more GSRN numbers within a specified
    period of time. Includes both the individual declaration and the general
    (for Denmark) in the same period.

    Endpoint docs:
    """

    # TODO Enter your GSRN number(s) here (replace GSRN1 and GSRN2):
    gsrn = ['GSRN1', 'GSRN2']
    gsrn = [ '571313180400240612']

    response = requests.post(
        url=f'{ACCOUNT_SERVICE_URL}/eco-declaration',
        headers={'Authorization': 'Bearer %s' % session['token']},
        verify=False,
        json={
            'gsrn': gsrn,
            'resolution': 'month',
            'utcOffset': 2,
            'beginRange': {
                'begin': '2019-01-01 00:00',
                'end': '2020-12-31 23:00'
            },
        },
    )

    response_json = response.json()

    env = {
        'individual': response_json['individual'],
        'general': response_json['general'],
    }

    return render_template('environment-declaration.html', **env)
