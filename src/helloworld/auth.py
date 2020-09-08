from requests import get
from flask import url_for
from authlib.jose import jwt
from authlib.integrations.requests_client import OAuth2Session

from helloworld.settings import (
    PROJECT_URL,
    OAUTH2_CLIENT_ID,
    OAUTH2_CLIENT_SECRET,
    OAUTH2_SCOPES,
    OAUTH2_LOGIN_ENDPOINT,
    OAUTH2_TOKEN_ENDPOINT,
    OAUTH2_WELLKNOWN_ENDPOINT,
)


client = OAuth2Session(
    client_id=OAUTH2_CLIENT_ID,
    client_secret=OAUTH2_CLIENT_SECRET,
    scope=OAUTH2_SCOPES,
)


def get_callback_url():
    """
    :rtype: str
    """
    callback_path = url_for('login-callback')
    callback_url = '%s%s' % (PROJECT_URL, callback_path)
    return callback_url


def register_login_state():
    """
    :rtype: (str, str)
    :returns: Tuple of (login_url, state)
    """
    return client.create_authorization_url(
        url=OAUTH2_LOGIN_ENDPOINT,
        redirect_uri=get_callback_url(),
    )


def fetch_token(code, state):
    """
    :param str code:
    :param str state:
    :rtype: collections.abc.Mapping
    """
    return client.fetch_token(
        url=OAUTH2_TOKEN_ENDPOINT,
        grant_type='authorization_code',
        code=code,
        state=state,
        redirect_uri=get_callback_url(),
        verify=False,  # TODO verify=True ?
    )


def parse_id_token(id_token):
    """
    :param str id_token:
    :rtype: collections.abc.Mapping
    """
    return jwt.decode(id_token, key=get_jwks())


def get_jwks():
    """
    TODO cache?

    :rtype: str
    """
    response = get(url=OAUTH2_WELLKNOWN_ENDPOINT, verify=False)  # TODO verify=True ?
    return response.content.decode()
