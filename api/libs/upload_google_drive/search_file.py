from __future__ import print_function

import logging
from ..utils.logging_helper import setup_logging

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

setup_logging()
logger = logging.getLogger(__name__)


def search_file():
    """Search file in drive location

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        files = []
        page_token = None
        while True:
            # pylint: disable=maybe-no-member
            response = service.files().list(q="mimeType='image/jpeg'",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                logger.info('Found file: %s, %s', file.get("name"), file.get("id"))
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
        logger.error('An error occurred: %s', error)
        files = None

    return files
