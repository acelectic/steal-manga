
import pprint

from bson import ObjectId
from pymongo import ReplaceOne, ReturnDocument, UpdateOne
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .constants import DB_NAME, DB_PASSWORD, DB_USERNAME
from .interface import MangaUploadedToDrive, UpdateMangaConfigData

uri: str = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_NAME}.nlqv7lj.mongodb.net/?retryWrites=true&w=majority"

db_client: MongoClient | None = None


def get_db_client() -> MongoClient:
    """Create a MongoDB client lazily."""
    global db_client
    if db_client is None:
        db_client = MongoClient(
            uri,
            server_api=ServerApi('1'),
            connectTimeoutMS=60 * 1000,
        )
        try:
            db_client.admin.command('ping')
        except Exception as e:  # pragma: no cover - connection may fail in CI
            print(e)
    return db_client


class StealMangaDb:
    """ StealMangaDb """

    db_name = DB_NAME
    table_name_manga_config = 'manga_configs'
    table_name_manga_upload = 'manga_uploads'
    table_name_google_token = 'google_tokens'

    google_token_id = 'google_token'

    def __init__(self) -> None:
        client = get_db_client()
        self.steal_manga_db = client.get_database(self.db_name)
        list_collection_names = self.steal_manga_db.list_collection_names()

        # create_collection if not exists
        if self.table_name_manga_config not in list_collection_names:
            self.steal_manga_db.create_collection(self.table_name_manga_config)

        if self.table_name_manga_upload not in list_collection_names:
            self.steal_manga_db.create_collection(self.table_name_manga_upload)

        if self.table_name_google_token not in list_collection_names:
            self.steal_manga_db.create_collection(self.table_name_google_token)

        # assign collection
        self.table_manga_config = self.steal_manga_db[self.table_name_manga_config]
        self.table_manga_upload = self.steal_manga_db[self.table_name_manga_upload]
        self.table_google_token = self.steal_manga_db[self.table_name_google_token]

    def replace_google_token(self, token_json: dict):
        if token_json is not None:
            token_json['_id'] = self.google_token_id
            return self.table_google_token.find_one_and_replace(
                filter={
                    "_id": self.google_token_id
                },
                replacement=token_json,
                return_document=ReturnDocument.AFTER,
                upsert=True
            )

    def get_google_token(self):
        return self.table_google_token.find_one(filter={
            "_id": self.google_token_id
        })

    def delete_google_token(self):
        return self.table_google_token.delete_one({
            '_id': self.google_token_id
        })

    def get_manga_config(self, config_id: str):
        """ get_manga_config """

        manga_config = self.table_manga_config.find_one({
            "_id": ObjectId(config_id)
        })
        if manga_config is not None:
            return UpdateMangaConfigData(
                cartoon_name=manga_config['cartoon_name'],
                cartoon_id=manga_config['cartoon_id'],
                latest_chapter=manga_config['latest_chapter'],
                max_chapter=manga_config['max_chapter'],
                disabled=manga_config['disabled'],
                downloaded=manga_config['downloaded'],
                project_name=manga_config['project_name'],
                cartoon_drive_id=manga_config['cartoon_drive_id'],
            )

    def __clone_manga_config(self):
        manga_configs = self.table_manga_config.find()
        bulk_requests = []
        for d in manga_configs:
            new_d = {
                "cartoon_name": d['cartoon_name'],
                "cartoon_id": d['cartoon_id'],
                "latest_chapter": d['latest_chapter'],
                "max_chapter": d['max_chapter'],
                "disabled": d['disabled'],
                "downloaded": d['downloaded'],
                "project_name": d['project_name'],
                "cartoon_drive_id": d['cartoon_drive_id'],
            }
            new_d['cartoon_id'] = str(new_d['cartoon_id'])
            bulk_requests.append(
                ReplaceOne(
                    filter={
                        "project_name": d['project_name'],
                        "cartoon_id": d['cartoon_id']
                    },
                    replacement=new_d,
                    upsert=True,
                )
            )
        self.steal_manga_db['manga_configs'].bulk_write(bulk_requests)
        return


def get_manga_config(project_name: str = ''):
    """ get_manga_config """
    where = None
    if project_name != '':
        where = {
            "project_name": project_name
        }
    steal_manga_db = StealMangaDb()
    results = steal_manga_db.table_manga_config.find(where)
    data: list[UpdateMangaConfigData] = []
    for d in results:
        data.append(UpdateMangaConfigData(
            cartoon_name=d['cartoon_name'],
            cartoon_id=d['cartoon_id'],
            latest_chapter=d['latest_chapter'],
            max_chapter=d['max_chapter'],
            disabled=d['disabled'],
            downloaded=d['downloaded'],
            project_name=d['project_name'],
            cartoon_drive_id=d['cartoon_drive_id'],
            latest_sync=d['latest_sync'],
        ))
    return data


def get_manga_uploaded(where=None):
    steal_manga_db = StealMangaDb()
    results = steal_manga_db.table_manga_upload.find(where)

    data: list[MangaUploadedToDrive] = []
    for x in results:
        data.append(MangaUploadedToDrive(
            project_name=x['project_name'],
            project_drive_id=x['project_drive_id'],
            cartoon_id=x['cartoon_id'],
            cartoon_name=x['cartoon_name'],
            cartoon_drive_id=x['cartoon_drive_id'],
            manga_chapter_name=x['manga_chapter_name'],
            manga_chapter_drive_id=x['manga_chapter_drive_id'],
            created_time=x['created_time'],
            modified_by_me_time=x['modified_by_me_time'],
            viewed_by_me=x['viewed_by_me'],
        ))
    return data


def get_count_manga_downloaded():
    steal_manga_db = StealMangaDb()
    count_manga_downloaded = steal_manga_db.table_manga_upload.aggregate([
        {"$group": {"_id": "$cartoon_id", "downloaded": {"$sum": 1}}}
    ])
    count_manga_downloaded_hash: dict[str, int] = {}
    for d in count_manga_downloaded:
        count_manga_downloaded_hash[d['_id']] = d['downloaded']

    return count_manga_downloaded_hash


def update_manga_downloaded():
    print('update_manga_downloaded')
    steal_manga_db = StealMangaDb()
    count_manga_downloaded = steal_manga_db.table_manga_upload.aggregate([
        {"$group": {"_id": "$cartoon_id", "downloaded": {"$sum": 1}}}
    ])

    requests = [UpdateOne(
        filter={
                "cartoon_id": d['_id'],
                },
        update={
            '$set': {
                "downloaded": d['downloaded']
            }
        },
        upsert=False
    ) for d in count_manga_downloaded]
    results = steal_manga_db.table_manga_upload.bulk_write(requests)
    print('update_manga_downloaded end')

    return results
