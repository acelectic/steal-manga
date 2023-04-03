""" Main Module """
import os
import sys
sys.path.append("../libs")

from libs.utils.constants import CARTOON_DIR
from libs.upload_google_drive import generate_drive_manga_exists, upload_to_drive

if __name__ == "__main__":
    generate_drive_manga_exists()
    upload_to_drive()
    generate_drive_manga_exists(force_update=True)
    
