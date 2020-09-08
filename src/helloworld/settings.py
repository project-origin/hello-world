import os


# -- OAuth2 client -----------------------------------------------------------

# TODO: Paste the Client ID here:
OAUTH2_CLIENT_ID = ''

# TODO: Paste the Secret here:
OAUTH2_CLIENT_SECRET = ''

OAUTH2_URL = 'https://oauth.eloprindelse.dk'
OAUTH2_LOGIN_ENDPOINT = f'{OAUTH2_URL}/oauth2/auth'
OAUTH2_LOGOUT_ENDPOINT = f'{OAUTH2_URL}/oauth2/sessions/logout'
OAUTH2_TOKEN_ENDPOINT = f'{OAUTH2_URL}/oauth2/token'
OAUTH2_WELLKNOWN_ENDPOINT = f'{OAUTH2_URL}/.well-known/jwks.json'

OAUTH2_SCOPES = (
    'openid',
    'offline',
    'profile',
    'email',
    'meteringpoints.read',
    'measurements.read',
    'ggo.read',
    'ggo.transfer',
    'ggo.retire',
)


# -- Project -----------------------------------------------------------------

PROJECT_HOST = '127.0.0.1'
PROJECT_PORT = 6789
PROJECT_URL = f'http://{PROJECT_HOST}:{PROJECT_PORT}'
PROJECT_SECRET = 'H#"(DF"(#YUFrghiu3ghf8y3egfoI(#GIfuagfeIOGAISJghasdkjhgfASD'


# -- Services ----------------------------------------------------------------

DATAHUB_SERVICE_URL = 'https://datahub.eloprindelse.dk/'
ACCOUNT_SERVICE_URL = 'https://account.eloprindelse.dk/'

# -- Folders/directories -----------------------------------------------------

__current_file = os.path.abspath(__file__)
__current_folder = os.path.split(__current_file)[0]


# Path to /src folder
SOURCE_DIR = os.path.abspath(os.path.join(__current_folder, '..'))

# Path to /src/templates folder
TEMPLATES_DIR = os.path.join(SOURCE_DIR, 'templates')
