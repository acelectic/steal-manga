"""
    Constants
"""
import os
from typing import List

from dotenv import load_dotenv

from .file_helper import get_env, get_env_str_array

load_dotenv()

cwd = os.getcwd()

MAN_MIRROR = 'man-mirror'
MY_NOVEL = 'my-novel'

GOOGLE_AUTH_TOKEN_PATH = os.path.join(cwd, 'config/token.json')
MANGA_ROOT_DIR = os.path.join(cwd, 'config/manga')
CARTOON_DIR = os.path.join(cwd, 'files/cartoons')

DRIVE_CARTOONS_DIR_ID: str = get_env('DRIVE_CARTOONS_DIR_ID') or ''
UPDATE_MINUTE_THRESHOLD = int(get_env('UPDATE_MINUTE_THRESHOLD') or 1)
DELETE_FILE_AFTER_UPLOADED: bool = get_env('DELETE_FILE_AFTER_UPLOADED') == 'true'

APP_URL: str = get_env('APP_URL') or ''
WEB_URL: str = get_env('WEB_URL') or ''

GOOGLE_AUTH_TYPE: str = get_env('GOOGLE_AUTH_TYPE') or ''
GOOGLE_CLIENT_ID: str = get_env('GOOGLE_CLIENT_ID') or ''
GOOGLE_PROJECT_ID: str = get_env('GOOGLE_PROJECT_ID') or ''
GOOGLE_CLIENT_SECRET: str = get_env('GOOGLE_CLIENT_SECRET') or ''
GOOGLE_REDIRECT_URIS: List[str] = get_env_str_array('GOOGLE_REDIRECT_URIS')
GOOGLE_JAVASCRIPT_ORIGINS:  List[str] = get_env_str_array('GOOGLE_JAVASCRIPT_ORIGINS')


DB_USERNAME: str = get_env('DB_USERNAME') or ''
DB_PASSWORD: str = get_env('DB_PASSWORD') or ''

GOOGLE_CLIENT_CONFIG = {}
GOOGLE_CLIENT_CONFIG[GOOGLE_AUTH_TYPE] = {
    'client_id': GOOGLE_CLIENT_ID,
    'project_id': GOOGLE_PROJECT_ID,
    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'token_uri': 'https://www.googleapis.com/oauth2/v3/token',
    'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
    'client_secret': GOOGLE_CLIENT_SECRET,
    'redirect_uris': GOOGLE_REDIRECT_URIS,
    'javascript_origins': GOOGLE_JAVASCRIPT_ORIGINS
}
