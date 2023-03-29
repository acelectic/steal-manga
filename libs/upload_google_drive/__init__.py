# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function
import sys
# sys.path.append("../../..")  # Adds higher directory to python modules path.

from .google_auth import authen
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
import glob
from ..utils.constants import CARTOON_DIR
# sys.path.append(".")  # Adds higher directory to python modules path.


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def upload_all():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = authen()
    if creds == None:
        print('not authen')
        return

    try:
        projects = upload_cartoons()
        print(f'projects: {projects}')
        return 
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def upload_cartoons():
    projects = []
    for project_dir in os.listdir(f'{CARTOON_DIR}'):
        # for name in files:
        #     print(os.path.join(root, name))
        if project_dir == None:
            continue
        title = project_dir

        sub_dirs = []

        for sub_project_cartoon_dir in os.listdir(os.path.join(CARTOON_DIR, project_dir)):
            print(f'{sub_project_cartoon_dir}')
            if sub_project_cartoon_dir == None:
                continue
            image_pdf_list = glob.glob(os.path.join(
                CARTOON_DIR, project_dir, sub_project_cartoon_dir, '*.pdf'))
            sub_dirs.append({
                "title": sub_project_cartoon_dir,
                "image_pdf_list": image_pdf_list
            })

        projects.append({
            "title": title,
            "sub_dirs": sub_dirs
        })
    return projects
