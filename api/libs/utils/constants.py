"""
    Constants
"""
import os

from dotenv import load_dotenv

from .file_helper import get_env

# sys.path.append('../utils')
# sys.path.append('../../libs')

load_dotenv()

cwd = os.getcwd()

GOOGLE_AUTH_TOKEN_PATH = os.path.join(cwd, 'config/token.json')
MANGE_ROOT_DIR = os.path.join(cwd, 'config/manga')
CARTOON_DIR = os.path.join(cwd, 'files/cartoons')
MANGE_EXISTS_FILE_PATH = os.path.join(CARTOON_DIR, 'manga_exists.json')
UPDATE_TIMESTAMP_FILE_PATH = os.path.join(CARTOON_DIR, 'update_timestamp.txt')

DRIVE_CARTOONS_DIR_ID: str = get_env('DRIVE_CARTOONS_DIR_ID') or ''
UPDATE_MINUTE_THRESHOLD = int(get_env('UPDATE_MINUTE_THRESHOLD') or 1)
DELETE_FILE_AFTER_UPLOADED: bool = get_env('DELETE_FILE_AFTER_UPLOADED') == 'true'
