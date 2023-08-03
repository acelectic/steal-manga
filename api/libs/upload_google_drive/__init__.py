# -*- coding: utf-8 -*-
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

import glob
import json
import os
import pprint
import shutil
import sys
from datetime import datetime
from typing import Any, Dict, List

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from tqdm import tqdm

from ..utils.constants import (
    CARTOON_DIR,
    DELETE_FILE_AFTER_UPLOADED,
    DRIVE_CARTOONS_DIR_ID,
    MANGE_EXISTS_FILE_PATH,
    UPDATE_MINUTE_THRESHOLD,
    UPDATE_TIMESTAMP_FILE_PATH,
)
from ..utils.file_helper import mkdir
from .google_auth import authen
from .interface import ProjectCartoonItem, ProjectItem

# sys.path.append("../../libs")  # Adds higher directory to python modules path.
# sys.path.append("../utils")


# sys.path.append(".")  # Adds higher directory to python modules path.


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def upload_to_drive(project_name=None, cartoon_name=None, logging=False):
    """
        Upload to drive
    """
    try:
        cartoon_projects = get_cartoon_projects()
        service = get_drive_service()

        # drive_project_dirs = list_drive_dirs(service, drive_cartoons_dir_id)
        # Call the Drive v3 API
        # results = service.files().list(
        #     q = "mimeType = 'application/vnd.google-apps.folder' and trashed=false",
        #     spaces='drive',
        #     pageSize=50, fields="nextPageToken, files(id, name)").execute()
        # items = results.get('files', [])

        # project level
        # print('\n[Process]: START upload_to_drive\n')
        for cartoon_project in cartoon_projects[::]:
            cartoon_project_res = find_or_init_dir(
                service, DRIVE_CARTOONS_DIR_ID, cartoon_project.title)

            if cartoon_project_res is not None:
                cartoon_project_id, cartoon_project_dir = cartoon_project_res

                if project_name is not None and project_name != cartoon_project_dir.get("name"):
                    # print(f'skip project_name: {project_name} {project_dir["name"]}')
                    continue

                if logging:
                    print(f'dir_id: {cartoon_project_id}, dir: {cartoon_project_dir.get("name")}')

                sub_dir_list = cartoon_project.sub_dirs[::]
                sub_dir_files = [
                    manga_file for cartoon_project_sub_dir in sub_dir_list for manga_files in cartoon_project_sub_dir.image_pdf_list for manga_file in manga_files]
                if len(sub_dir_list) <= 0 or len(sub_dir_files) <= 0:
                    continue

                print(f'[Process]: UPLOAD Project {cartoon_project_dir.get("name")}')
                # manga level
                for cartoon_project_sub_dir in sub_dir_list:
                    cartoon_project_sub_dir_res = find_or_init_dir(
                        service, cartoon_project_id, cartoon_project_sub_dir.title)

                    if cartoon_project_sub_dir_res is not None:
                        sub_dir_id, sub_dir = cartoon_project_sub_dir_res
                        manga_name = sub_dir.get("name")

                        if cartoon_name is not None and cartoon_name != manga_name:
                            # print(f'skip cartoon_name: {cartoon_name} {manga_dir["name"]}')
                            continue

                        if logging:
                            print(f'\tdir_id: {sub_dir_id}, dir: {manga_name}')
                        else:
                            print(f'[Process]: UPLOAD Manga {manga_name}')

                        manga_files = cartoon_project_sub_dir.image_pdf_list[::]
                        total_files = len(manga_files)

                        if total_files > 0:
                            # upload manga
                            for image_pdf in tqdm(manga_files,
                                                  desc=f'[Process]: UPLOAD {manga_name}',
                                                  total=total_files):
                                file_name = image_pdf.split('/')[-1]
                                file_path = image_pdf

                                upload_file(
                                    service, logging, sub_dir_id, file_name, file_path)

        # if not drive_project_dirs:
        #     print('No files found.')
        #     return
        # print('Files:')
        # for project_dir in drive_project_dirs[::]:
        #     print(u'{0} ({1})'.format(project_dir['name'], project_dir['id']))
        #     drive_project_manga_dirs = list_drive_dirs(service, project_dir['id'])
        #     for manga_dir in drive_project_manga_dirs[::]:
        #         print(u'\t{0} ({1})'.format(manga_dir['name'], manga_dir['id']))
        #         drive_manga_chapters = list_drive_manga(service, manga_dir['id'])
        #         for drive_manga_chapter in drive_manga_chapters[::]:
        #             print(u'\t\t{0} ({1})'.format(drive_manga_chapter['name'], drive_manga_chapter['id']))

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def upload_file(service, logging: bool, sub_dir_id: str, file_name: str, file_path: str) -> None:
    upload_manga_res = upload_file_to_drive_if_not_exists(
        service, file_name, file_path, sub_dir_id)

    if upload_manga_res is not None:
        file_id, file = upload_manga_res
        if logging:
            print(f'\t\tfile_id: {file_id}, file: {file.get("name")}')
        delete_file(file_path)
    else:
        pprint.pprint({
            "tag": "upload_file error"
        })


def generate_drive_manga_exists(project_name=None, cartoon_name=None, force_update=False, logging=False) -> Dict[Any, Any]:
    """
        get and generate manga in drive
    """
    manga_exists_json = {}
    is_early_update = False

    print(f'generate_drive_manga_exists | {project_name or "all"} {cartoon_name or ""}')

    try:
        if os.path.exists(UPDATE_TIMESTAMP_FILE_PATH):
            with open(UPDATE_TIMESTAMP_FILE_PATH, "r", encoding='utf-8') as read_file:
                update_timestamp = read_file.read()
                if update_timestamp is not None:
                    now = datetime.now()
                    timestamp = datetime.fromtimestamp(float(update_timestamp), tz=None)
                    print(f'last update manga exists: {timestamp.strftime("%Y-%m-%d %H:%M:%S")}')
                    time_diff = now - timestamp
                    if time_diff.total_seconds() / 60 < UPDATE_MINUTE_THRESHOLD:
                        is_early_update = True

        # Opening JSON file
        if os.path.exists(MANGE_EXISTS_FILE_PATH):
            with open(MANGE_EXISTS_FILE_PATH, "r", encoding='utf-8') as read_file:
                manga_exists_json = json.load(read_file)

        if is_early_update and not force_update:
            return manga_exists_json

        service = get_drive_service()
        drive_project_dirs = list_drive_dirs(service, DRIVE_CARTOONS_DIR_ID)

        if not drive_project_dirs:
            print('No files found.')
            return manga_exists_json

        if logging:
            print('Files:')
        for project_dir in drive_project_dirs[::]:
            if project_name is not None and project_name != project_dir['name']:
                # print(f'skip project_name: {project_name} {project_dir["name"]}')
                continue

            if logging:
                print('{0} ({1})'.format(project_dir['name'], project_dir['id']))

            manga_exists_json[project_dir['name']] = {
                "id": project_dir['id'],
                "sub_dirs": {}
            }

            drive_project_manga_dirs = list_drive_dirs(
                service, project_dir['id'])
            for manga_dir in drive_project_manga_dirs[::]:
                if cartoon_name is not None and cartoon_name != manga_dir['name']:
                    # print(f'skip cartoon_name: {cartoon_name} {manga_dir["name"]}')
                    continue

                if logging:
                    print('\t{0} ({1})'.format(
                        manga_dir['name'], manga_dir['id']))

                drive_manga_chapters = list_drive_manga(
                    service, manga_dir['id'])

                manga_exists_json[project_dir['name']]["sub_dirs"][manga_dir['name']] = {
                    "id": manga_dir['id'],
                    'total':  len(drive_manga_chapters),
                    "chapters": {}
                }

                for drive_manga_chapter in drive_manga_chapters[::]:
                    if logging:
                        print(f'\t\t{drive_manga_chapter["name"]} ({drive_manga_chapter["id"]})')
                    manga_exists_json[project_dir['name']]["sub_dirs"][manga_dir['name']]["chapters"][drive_manga_chapter['name']] = {
                        "id": drive_manga_chapter['id'],
                        "createdTime": drive_manga_chapter['createdTime'],
                        "modifiedByMeTime": drive_manga_chapter['modifiedByMeTime'],
                        "viewedByMe": drive_manga_chapter['viewedByMe'],
                    }

                manga_exists_json[project_dir['name']]["sub_dirs"][manga_dir['name']]["chapters"] = order_keys_in_json(
                    manga_exists_json[project_dir['name']]["sub_dirs"][manga_dir['name']]["chapters"])
            manga_exists_json[project_dir['name']]["sub_dirs"] = order_keys_in_json(
                manga_exists_json[project_dir['name']]["sub_dirs"])
        manga_exists_json = order_keys_in_json(manga_exists_json)

        # Serializing json
        json_object = json.dumps(manga_exists_json, indent=2, ensure_ascii=False)

        if not os.path.exists(CARTOON_DIR):
            mkdir(CARTOON_DIR)
        
        # Writing to sample.json
        with open(MANGE_EXISTS_FILE_PATH, "w", encoding='utf-8') as outfile:
            outfile.write(json_object)

        with open(UPDATE_TIMESTAMP_FILE_PATH, "w", encoding='utf-8') as outfile:
            # Getting the current date and time
            dt = datetime.now()

            # getting the timestamp
            ts = datetime.timestamp(dt)
            outfile.write(str(ts))

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

    return manga_exists_json


def get_drive_service():
    creds = authen()
    if creds is None:
        print('not authen')
        return

    service = build('drive', 'v3', credentials=creds)
    return service


def list_drive_dirs(service, drive_cartoons_dir_id: str):
    page_token = None
    drive_project_dirs = []
    while True:
        # pylint: disable=maybe-no-member
        response = service.files().list(
            q=f"'{drive_cartoons_dir_id}' in parents and trashed=false",
            spaces='drive',
            fields='nextPageToken, '
            'files(id, name)',
            pageToken=page_token).execute()

        drive_project_dirs.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return drive_project_dirs


def list_drive_manga(service, drive_cartoons_dir_id: str):
    page_token = None
    drive_project_dirs = []
    while True:
        # pylint: disable=maybe-no-member
        response = service.files().list(
            q=f"'{drive_cartoons_dir_id}' in parents and trashed=false",
            spaces='drive',
            fields='nextPageToken, '
            'files(id, name, createdTime, modifiedByMeTime, viewedByMe)',
            pageToken=page_token).execute()

        drive_project_dirs.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    # print(f'\n{json.dumps(drive_project_dirs[:1:])}\n')
    return drive_project_dirs


def upload_file_to_drive_if_not_exists(service, file_name: str, file_path: str, folder_id: str):
    try:
        dir_result = None
        dir_res = service.files().list(
            q=f"'{folder_id}' in parents and name='{file_name}' and mimeType='application/pdf' and trashed=false",
            spaces='drive',
            fields='nextPageToken, '
            'files(id, name, createdTime, modifiedByMeTime, viewedByMe)',
        ).execute()
        # pprint.pprint({
        #     "dir_res": dir_res
        # })
        if dir_res is not None and dir_res['files'] is not None and len(dir_res['files']) > 0:
            dir_result = dir_res['files'][0]
        # print(dir_result)
        if dir_result is None:
            return upload_file_to_drive(service, file_name, file_path, folder_id)
        return dir_result.get('id'), dir_result
    except Exception as error:
        pprint.pprint({
            "tag": "upload_file_to_drive_if_not_exists",
            "error": error
        })
        return None


def upload_file_to_drive(service, file_name: str, file_path: str, folder_id: str):
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path,
                            mimetype='application/pdf',
                            resumable=True)

    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id, name').execute()
    # pprint.pprint({
    #     "tag": "upload",
    #     "file": file,
    #     "file_metadata": file_metadata
    # })
    return file['id'], file


def get_cartoon_projects() -> List[ProjectItem]:
    """ get_cartoon_projects """
    projects: List[ProjectItem] = []
    for project_dir in os.listdir(f'{CARTOON_DIR}'):
        # for name in files:
        #     print(os.path.join(root, name))
        project_dir_path = os.path.join(CARTOON_DIR, project_dir)
        if project_dir is None or not os.path.isdir(project_dir_path):
            continue
        title = project_dir

        sub_dirs: List[ProjectCartoonItem] = []

        for sub_project_cartoon_dir in os.listdir(project_dir_path):
            # print(f'{sub_project_cartoon_dir}')
            if sub_project_cartoon_dir is None:
                continue
            image_pdf_list = glob.glob(os.path.join(
                CARTOON_DIR, project_dir, sub_project_cartoon_dir, '*.pdf'))
            sub_dirs.append(ProjectCartoonItem(
                sub_project_cartoon_dir, image_pdf_list))

        projects.append(ProjectItem(title, sub_dirs=sub_dirs))
    return projects


def find_or_init_dir(service, drive_cartoons_dir_id: str, dir_name: str):
    """ find_or_init_dir """
    dir_file = None
    dir_res = service.files().list(
        q=f"'{drive_cartoons_dir_id}' in parents and name='{dir_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        spaces='drive',
        fields='nextPageToken, '
        'files(*)',
    ).execute()
    # print(f'dir_res: {dir_res}')
    if dir_res is not None and dir_res['files'] is not None and len(dir_res['files']) > 0:
        dir_file = dir_res['files'][0]
    # print(dir)
    # print(f'dir_name: {dir_name}')
    # print(dir)
    if dir_file is None:
        return create_folder(service, drive_cartoons_dir_id, dir_name)
    return dir_file.get('id'), dir_file


def create_folder(service, parent_dir_id: str, dir_name: str):
    """ Create a folder and prints the folder ID
    Returns : Folder Id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        # create drive api client
        file_metadata = {
            'name': dir_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_dir_id]
        }

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields='files(id, name)'
                                      ).execute()
        # print(F'Create Folder ID: "{file.get("id")}".')
        return file.get('id'), file

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


def delete_file(file_path: str):
    """
        Delete file after upload to drive
    """
    if os.path.exists(file_path):
        if DELETE_FILE_AFTER_UPLOADED:
            os.remove(file_path)
        else:
            trash_dir = os.path.join(
                'files', 'trash', '/'.join(file_path.split('/')[2:-1:]))
            # print(f'trash_dir: {trash_dir}')
            mkdir(trash_dir)
            new_path = os.path.join(trash_dir, file_path.split('/')[-1])
            shutil.move(file_path, new_path)


def order_keys_in_json(data: dict) -> dict:
    """ order_keys_in_json """
    return dict(sorted(data.items(), key=lambda x: str(x[0]).zfill(30)))
