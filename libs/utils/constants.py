"""
    Constants
"""
import os
from typing import LiteralString

from dotenv import load_dotenv

from .file_helper import get_env

# sys.path.append('../utils')
# sys.path.append('../../libs')

load_dotenv()

CARTOON_DIR = 'files/cartoons'
MANGE_EXISTS_FILE_PATH: LiteralString = os.path.join(CARTOON_DIR, 'manga_exists.json')
UPDATE_TIMESTAMP_FILE_PATH: LiteralString = os.path.join(CARTOON_DIR, 'update_timestamp.txt')

GOOGLE_DRIVE_DIR: str = get_env('GOOGLE_DRIVE_DIR') or ''
DRIVE_CARTOONS_DIR_ID: str = get_env('DRIVE_CARTOONS_DIR_ID') or ''
UPDATE_MINUTE_THRESHOLD = int(get_env('UPDATE_MINUTE_THRESHOLD') or 1)
DELETE_FILE_AFTER_UPLOADED: bool = get_env('DELETE_FILE_AFTER_UPLOADED') == 'true'
