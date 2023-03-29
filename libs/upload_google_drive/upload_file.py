from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def upload_to_folder(folder_id, file_name: str, file_path: str, mimetype='application/pdf'):
    """Upload a file to the specified folder and prints file ID, folder ID
    Args: Id of the folder
    Returns: ID of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path,
                                mimetype=mimetype, resumable=True)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: "{file.get("id")}".')
        return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None
