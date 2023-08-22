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

# [START drive_quickstart]
from __future__ import print_function

import os

from google.auth import external_account_authorized_user
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from ..utils.constants import APP_URL, GOOGLE_AUTH_TOKEN_PATH, GOOGLE_CLIENT_CONFIG

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']




def get_google_flow(redirect_uri=f'{APP_URL}/google-callback') -> InstalledAppFlow:
    """ get_google_flow """
    
    print(f'redirect_uri: {redirect_uri}')
    return InstalledAppFlow.from_client_config(
        client_config=GOOGLE_CLIENT_CONFIG, scopes=SCOPES, redirect_uri=redirect_uri)


def authen():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(GOOGLE_AUTH_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(
            GOOGLE_AUTH_TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                if os.path.exists(GOOGLE_AUTH_TOKEN_PATH):
                    os.remove(GOOGLE_AUTH_TOKEN_PATH)
                return authen()
        else:
            flow = get_google_flow()
            creds = flow.run_local_server(port=0)

        write_google_token(creds)

    return creds


def write_google_token(creds: external_account_authorized_user.Credentials | Credentials):
    if creds:
        # Save the credentials for the next run
        with open(GOOGLE_AUTH_TOKEN_PATH, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())


def get_google_creds():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(GOOGLE_AUTH_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(
            GOOGLE_AUTH_TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                if os.path.exists(GOOGLE_AUTH_TOKEN_PATH):
                    os.remove(GOOGLE_AUTH_TOKEN_PATH)
    return creds
