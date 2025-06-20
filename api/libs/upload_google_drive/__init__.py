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

import logging
import datetime
import glob
import os
import shutil
from typing import List

from bson import DatetimeConversion, ObjectId
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from pymongo import DeleteMany, DeleteOne, ReplaceOne, ReturnDocument, UpdateOne
from tqdm import tqdm

from ..utils.constants import (
    CARTOON_DIR,
    DELETE_FILE_AFTER_UPLOADED,
    DRIVE_CARTOONS_DIR_ID,
    LOG_LEVEL,
)
from ..utils.db_client import (
    StealMangaDb,
    get_manga_config,
    get_manga_uploaded,
    update_manga_downloaded,
)
from ..utils.logging_helper import setup_logging
from ..utils.file_helper import mkdir
from ..utils.interface import MangaUploadedToDrive, UpdateMangaConfigData
from .google_auth import authen
from .interface import ProjectCartoonItem, ProjectItem

# sys.path.append("../../libs")  # Adds higher directory to python modules path.
# sys.path.append("../utils")


# sys.path.append(".")  # Adds higher directory to python modules path.


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

setup_logging()
logger = logging.getLogger(__name__)


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

        steal_manga_db = StealMangaDb()
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
                    logger.info('dir_id: %s, dir: %s', cartoon_project_id, cartoon_project_dir.get("name"))

                sub_dir_list = cartoon_project.sub_dirs[::]
                sub_dir_files = [
                    manga_file for cartoon_project_sub_dir in sub_dir_list for manga_files in cartoon_project_sub_dir.image_pdf_list for manga_file in manga_files]
                if len(sub_dir_list) <= 0 or len(sub_dir_files) <= 0:
                    continue

                logger.info('[Process]: UPLOAD Project %s', cartoon_project_dir.get("name"))
                # manga level
                for cartoon_project_sub_dir in sub_dir_list:
                    cartoon_project_sub_dir_res = find_or_init_dir(
                        service, cartoon_project_id, cartoon_project_sub_dir.title)

                    if cartoon_project_sub_dir_res is not None:
                        sub_dir_id, sub_dir = cartoon_project_sub_dir_res
                        manga_name = sub_dir.get("name")
                        manga_config = steal_manga_db.table_manga_config.find_one(
                            {
                                "cartoon_name": manga_name
                            },
                        )
                        logger.debug(manga_config)
                        if cartoon_name is not None and cartoon_name != manga_name:
                            # print(f'skip cartoon_name: {cartoon_name} {manga_dir["name"]}')
                            continue

                        if logging:
                            logger.info('\tdir_id: %s, dir: %s', sub_dir_id, manga_name)
                        else:
                            logger.info('[Process]: UPLOAD Manga %s', manga_name)

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
                            if manga_config is not None:
                                steal_manga_db.table_manga_config.update_one(
                                    {
                                        "_id": manga_config.get('_id')
                                    },
                                    {
                                        '$set': {
                                            "latest_sync": datetime.datetime.utcnow().isoformat()
                                        }
                                    })

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
        logger.error('An error occurred: %s', error)


def upload_file(service, logging: bool, sub_dir_id: str, file_name: str, file_path: str) -> None:
    upload_manga_res = upload_file_to_drive_if_not_exists(
        service, file_name, file_path, sub_dir_id)

    if upload_manga_res is not None:
        file_id, file = upload_manga_res
        if logging:
            logger.info('\t\tfile_id: %s, file: %s', file_id, file.get("name"))
        delete_file(file_path)
    else:
        logger.error({'tag': 'upload_file error'})


def generate_drive_manga_exists(target_project_name=None, target_cartoon_name=None, logging=False) -> list[MangaUploadedToDrive]:
    """
        get and generate manga in drive
    """
    logger.info(
        'generate_drive_manga_exists | %s %s',
        target_project_name or 'all',
        target_cartoon_name or ''
    )

    try:
        steal_manga_db = StealMangaDb()

        service = get_drive_service()
        drive_project_dirs = list_drive_dirs(service, DRIVE_CARTOONS_DIR_ID)
        all_manga_config = get_manga_config()
        all_manga_config_hash: dict[str, UpdateMangaConfigData] = {}

        manga_config_update_drive_id_list: list[UpdateMangaConfigData] = []
        manga_uploaded_to_drive: list[MangaUploadedToDrive] = []

        for d in all_manga_config:
            all_manga_config_hash[d.cartoon_name] = d

        if not drive_project_dirs:
            logger.info('No files found.')
            return []

        if logging:
            logger.info('Files:')
        for project_dir in drive_project_dirs[::]:
            if target_project_name is not None and target_project_name != project_dir['name']:
                # print(f'skip project_name: {project_name} {project_dir["name"]}')
                continue

            if logging:
                logger.info('%s (%s)', project_dir['name'], project_dir['id'])

            project_name = project_dir['name']
            project_drive_id = project_dir['id']

            drive_project_manga_dirs = list_drive_dirs(
                service, project_dir['id'])
            for manga_dir in drive_project_manga_dirs[::]:
                if target_cartoon_name is not None and target_cartoon_name != manga_dir['name']:
                    # print(f'skip cartoon_name: {cartoon_name} {manga_dir["name"]}')
                    continue
                cartoon_name = manga_dir['name']
                cartoon_drive_id = manga_dir['id']
                manga_config = all_manga_config_hash.get(cartoon_name)

                if manga_config is not None:
                    manga_config.cartoon_drive_id = cartoon_drive_id
                    manga_config_update_drive_id_list.append(manga_config)

                if logging:
                    logger.info('\t%s (%s)', manga_dir['name'], manga_dir['id'])

                drive_manga_chapters = list_drive_manga(
                    service, manga_dir['id'])

                for drive_manga_chapter in drive_manga_chapters[::]:
                    if logging:
                        logger.info('\t\t%s (%s)', drive_manga_chapter["name"], drive_manga_chapter["id"])

                    manga_chapter_name = drive_manga_chapter['name']
                    manga_chapter_drive_id = drive_manga_chapter['id']
                    created_time = drive_manga_chapter['createdTime']
                    modified_by_me_time = drive_manga_chapter['modifiedByMeTime']
                    viewed_by_me = drive_manga_chapter['viewedByMe']

                    manga_uploaded_to_drive.append(MangaUploadedToDrive(
                        project_name=project_name,
                        project_drive_id=project_drive_id,
                        cartoon_id=manga_config.cartoon_id if manga_config is not None else '',
                        cartoon_name=cartoon_name,
                        cartoon_drive_id=cartoon_drive_id,
                        manga_chapter_name=manga_chapter_name,
                        manga_chapter_drive_id=manga_chapter_drive_id,
                        created_time=created_time,
                        modified_by_me_time=modified_by_me_time,
                        viewed_by_me=viewed_by_me,
                    ))

        logger.info('manga_uploaded_to_drive: %s', len(manga_uploaded_to_drive))

        # update manga uploaded
        requests = [ReplaceOne(
            filter={
                "project_name": d.project_name,
                "cartoon_id": d.cartoon_id,
                "manga_chapter_name": d.manga_chapter_name,
            },
            replacement=d.to_json(),
            upsert=True
        ) for d in manga_uploaded_to_drive]
        steal_manga_db.table_manga_upload.bulk_write(requests)

        # remove cartoon deleted from drive
        remove_hash = {}
        for d in manga_uploaded_to_drive:
            key = f'{d.project_name}_{d.cartoon_id}'
            
            if remove_hash.get(key) is None:
                remove_hash[key] = {
                    "project_name": d.project_name,
                    "cartoon_id": d.cartoon_id,
                    "manga_chapter_names": []
                }
            
            remove_hash[key]["manga_chapter_names"].append(d.manga_chapter_name)
        

        for d in list(remove_hash.values()):

            should_delete_list = steal_manga_db.table_manga_upload.find({
                "project_name": d["project_name"],
                "cartoon_id": d["cartoon_id"],
                "manga_chapter_name": {
                    "$nin": d["manga_chapter_names"]
                },
            })

            for should_delete_item in should_delete_list:
                logger.debug({"should_delete_item": should_delete_item})
                deleted_item = steal_manga_db.table_manga_upload.delete_one({
                    "_id": ObjectId(should_delete_item["_id"])
                })
                logger.debug({"deleted_item": deleted_item})

        
        # update manga config
        update_config_requests: list[UpdateOne] = [UpdateOne(
            filter={
                "cartoon_id": d.cartoon_id,
            },
            update={
                '$set': d.to_json()
            },
            upsert=False,
        ) for d in manga_config_update_drive_id_list]
        steal_manga_db.table_manga_config.bulk_write(update_config_requests)

        update_manga_downloaded()

        if not os.path.exists(CARTOON_DIR):
            mkdir(CARTOON_DIR)

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        logger.error('An error occurred: %s', error)

    logger.info('generate_drive_manga_exists completed')
    return get_manga_uploaded()


def get_drive_service():
    creds = authen()
    if creds is None:
        logger.error('not authen')
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
        logger.error({'tag': 'upload_file_to_drive_if_not_exists', 'error': error})
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
        logger.error('An error occurred: %s', error)
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


def update_latest_sync(cartoon_id: str = ''):
    """ update_latest_sync """
    logger.info('update_latest_sync: %s', cartoon_id)
    where = {}
    if cartoon_id != '':
        where = {
            "cartoon_id": cartoon_id
        }

    steal_manga_db = StealMangaDb()
    manga_configs = steal_manga_db.table_manga_config.find(where)
    for manga_config in list(manga_configs):
        project_name = manga_config.get('project_name')
        cartoon_id = manga_config.get('cartoon_id')
        latest_manga_uploads = steal_manga_db.table_manga_upload.find({
            "project_name": project_name,
            "cartoon_id": cartoon_id,
        })
        latest_manga_uploads = sorted(
            latest_manga_uploads,
            key=lambda x: datetime.datetime.fromisoformat(str(x.get('created_time'))).timestamp(),
            reverse=True)  # type: ignore
        latest_manga_upload = latest_manga_uploads[0]
        if latest_manga_upload is not None:
            logger.debug({
                "project_name": project_name,
                "cartoon_id": cartoon_id,
            })
            # latest_manga_upload = steal_manga_db.table_manga_upload.find_one({
            #     "_id": latest_manga_upload.get('_id'),
            # })

            if latest_manga_upload is not None:
                created_time = latest_manga_upload.get('created_time')
                logger.debug({
                    "config_id": manga_config.get('_id'),
                    "created_time": created_time,
                    "latest_manga_upload": latest_manga_upload
                })
                manga_config_updated = steal_manga_db.table_manga_config.find_one_and_update(
                    filter={
                        "_id": manga_config.get('_id')
                        # "project_name": project_name,
                        # "cartoon_id": cartoon_id,
                    },
                    update={
                        "$set": {
                            "latest_sync":  datetime.datetime.fromisoformat(created_time)
                            # "latest_sync": created_time
                        }
                    },
                    return_document=ReturnDocument.AFTER,
                )
                logger.debug(manga_config_updated)
