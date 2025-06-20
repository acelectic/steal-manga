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

import logging

import json
import os

from google.auth import external_account_authorized_user
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from ..utils.constants import APP_URL, GOOGLE_AUTH_TOKEN_PATH, GOOGLE_CLIENT_CONFIG, LOG_LEVEL
from ..utils.logging_helper import setup_logging
from ..utils.db_client import StealMangaDb

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

steal_manga_db = StealMangaDb()
setup_logging()
logger = logging.getLogger(__name__)


def get_google_flow(redirect_uri=f'{APP_URL}/google-callback') -> InstalledAppFlow:
    """ get_google_flow """

    client_config = GOOGLE_CLIENT_CONFIG
    logger.debug('redirect_uri: %s', redirect_uri)

    return InstalledAppFlow.from_client_config(
        client_config=client_config, scopes=SCOPES, redirect_uri=redirect_uri)


def authen():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = __get_creds()

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                if os.path.exists(GOOGLE_AUTH_TOKEN_PATH):
                    os.remove(GOOGLE_AUTH_TOKEN_PATH)
                steal_manga_db.delete_google_token()
                return authen()
        else:
            flow = get_google_flow()
            creds = flow.run_local_server(port=0)
        write_google_token(creds)
    return creds


def write_google_token(creds: external_account_authorized_user.Credentials | Credentials):
    if creds:
        # Save the credentials for the next run
        token_json = creds.to_json()
        steal_manga_db.replace_google_token(json.loads(token_json))


def get_google_creds():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = __get_creds()

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                if os.path.exists(GOOGLE_AUTH_TOKEN_PATH):
                    os.remove(GOOGLE_AUTH_TOKEN_PATH)
                steal_manga_db.delete_google_token()
    return creds


def __get_creds():
    token_json = steal_manga_db.get_google_token()
    if token_json is not None:
        with open(GOOGLE_AUTH_TOKEN_PATH, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(token_json))

        return Credentials.from_authorized_user_file(
            GOOGLE_AUTH_TOKEN_PATH, SCOPES)
