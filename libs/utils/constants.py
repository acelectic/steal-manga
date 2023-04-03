"""
    Constants
"""
import os
from dotenv import load_dotenv

load_dotenv()

CARTOON_DIR = 'files/cartoons'
MANGE_EXISTS_FILE_PATH = os.path.join(CARTOON_DIR, 'manga_exists.json')
UPDATE_TIMESTAMP_FILE_PATH = os.path.join(CARTOON_DIR, 'update_timestamp.txt')

GOOGLE_DRIVE_DIR = os.getenv('GOOGLE_DRIVE_DIR') or ''
DRIVE_CARTOONS_DIR_ID = os.getenv('DRIVE_CARTOONS_DIR_ID') or ''
UPDATE_MINUTE_THRESHOLD = int(os.getenv('UPDATE_MINUTE_THRESHOLD') or 1)

assert GOOGLE_DRIVE_DIR != ''
assert DRIVE_CARTOONS_DIR_ID != ''
