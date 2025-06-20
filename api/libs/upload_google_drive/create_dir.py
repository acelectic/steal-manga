from __future__ import print_function

import logging
from ..utils.logging_helper import setup_logging

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_folder(dir_name: str):
    """ Create a folder and prints the folder ID
    Returns : Folder Id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    creds, _ = google.auth.default()

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        file_metadata = {
            'name': dir_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields='id'
                                      ).execute()
        logger.info('Folder ID: "%s".', file.get("id"))
        return file.get('id')
    except HttpError as error:
        logger.error('An error occurred: %s', error)
        return None
