"""
    Constants
"""
import sys
import os
from dotenv import load_dotenv

from libs.utils.file_helper import get_env

sys.path.append('../utils')
sys.path.append('../../libs')

load_dotenv()

CARTOON_DIR = 'files/cartoons'
MANGE_EXISTS_FILE_PATH = os.path.join(CARTOON_DIR, 'manga_exists.json')
UPDATE_TIMESTAMP_FILE_PATH = os.path.join(CARTOON_DIR, 'update_timestamp.txt')

GOOGLE_DRIVE_DIR = get_env('GOOGLE_DRIVE_DIR') or ''
DRIVE_CARTOONS_DIR_ID = get_env('DRIVE_CARTOONS_DIR_ID') or ''
UPDATE_MINUTE_THRESHOLD = int(get_env('UPDATE_MINUTE_THRESHOLD') or 1)
DELETE_FILE_AFTER_UPLOADED = get_env('DELETE_FILE_AFTER_UPLOADED') == 'true'
        